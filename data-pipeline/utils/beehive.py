import requests
from datetime import datetime
import re
from collections import namedtuple


def get_nodes():
    r = requests.get('http://beehive1.mcs.anl.gov/api/1/nodes/')

    for key, values in r.json()['data'].items():
        yield {
            'id': key.lower(),
            'name': values.get('name', '') or '',
            'description': values.get('description', '') or '',
            'tunnel-port': values.get('reverse_ssh_port', None),
        }


def get_export_dates(node_id):
    url = 'http://beehive1.mcs.anl.gov/api/1/nodes/{}/dates'.format(node_id.lower())
    r = requests.get(url)

    for date in r.json()['data']:
        try:
            yield datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            pass


Row = namedtuple('Row', ['node_id', 'date', 'plugin', 'timestamp', 'sensor', 'values'])
Plugin = namedtuple('Plugin', ['name', 'version', 'instance'])

date_format = '%Y-%m-%d'
timestamp_format = '%Y-%m-%d %H:%M:%S'
values_pattern = re.compile('\'([^\']+):([^\']+)\'')


def parse_export_date(s):
    return datetime.strptime(s, date_format)


def parse_export_timestamp(s):
    return datetime.strptime(s, timestamp_format)


def cleanup_key(s):
    return s.strip().lower()
    # return '-'.join(re.split('\s+|_+', s.strip().lower()))


def parse_export_values(s):
    return dict((cleanup_key(k), v) for (k, v) in values_pattern.findall(s))


def parse_export_line(line):
    row = list(map(str.strip, line.split(';')))

    return Row(row[0],
               parse_export_date(row[1]),
               Plugin(row[2], row[3], row[4]),
               parse_export_timestamp(row[5]),
               row[6],
               parse_export_values(row[8]))


def isentry(line):
    return line and not line.startswith('#')


def get_flat_export_data(node_id, date):
    url = 'http://beehive1.mcs.anl.gov/api/1/nodes/{}/export?date={}'.format(node_id, date)
    r = requests.get(url)

    for line in map(bytes.decode, r.iter_lines()):
        if line.startswith('#'):
            continue

        row = line.split(';')

        node_id = row[0]
        date = row[1]
        plugin_name = row[2]
        plugin_version = row[3]
        plugin_instance = row[4]

        timestamp = int(datetime.strptime(row[5], '%Y-%m-%d %H:%M:%S').timestamp())
        sensor = row[6]

        for k, v in values_pattern.findall(row[8]):
            yield node_id, timestamp, plugin_name, plugin_version, plugin_instance, sensor, k, v


def get_export_data(node_id, date):
    url = 'http://beehive1.mcs.anl.gov/api/1/nodes/{}/export?date={}'.format(node_id.lower(), date.strftime('%Y-%m-%d'))
    r = requests.get(url)
    return map(parse_export_line, filter(isentry, map(bytes.decode, r.iter_lines())))
