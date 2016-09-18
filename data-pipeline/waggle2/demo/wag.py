import requests
import pandas as pd
import numpy as np
import argparse
import json
from bokeh.layouts import layout, column
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.layouts import widgetbox
from bokeh.models.widgets import CheckboxButtonGroup, Panel, Tabs
from bokeh.io import curdoc
from bokeh.palettes import Spectral11
from bokeh.client import push_session


class DataSet:

    def __init__(self, node_id, dtype, sensor_names, dates):
        """
        :param node_id: str
        :param dtype: str
        :param sensor_names: [str]
        :param dates: str

        DataSet class. This class contains all the data for node and sensor type. node_id is the nodes unique id, dtype is the string
        data type for the node (e.g. 'Temperature', sensor names is the list of sensors with that data type, and date is the date of
        the data in YYYY-MM-DD format.
        """
        self.id = node_id
        self.dtype = dtype
        self.sensor_names = sensor_names
        self.dates = dates
        self.sources = {}
        self.used_sources = {}
        self.null_sources = {}
        self.cbg = CheckboxButtonGroup(labels=self.sensor_names, active=[i for i in range(len(self.sensor_names))])
        self.wb = widgetbox(self.cbg, width=600)
        self.plot = figure(title=self.dtype + ' data from node ' + self.id,
                           x_axis_type="datetime", tools="pan,wheel_zoom,box_zoom,reset,save,box_select")


    def get_sources(self, data):
        """
        :param data: pd.DataFrame()
        Loads and parses the general node data into DataSet's self.sources and self.used_sources data frame that only contains the data relevant for this
        nodes plotting.
        """
        for sens in self.sensor_names:
            filtered = data[(data['sensor'] == sens) & (data['id'] == self.id)].copy()

            #filtered = data[(data['sensor'] == sens) & (data['id'] == self.id) & (data['param'] == self.dtype)].copy()
            df = pd.DataFrame()
            df['t'] = filtered.time

            def GetValue(dictionary):
                if self.dtype in dictionary:
                    #print(self.dtype, dictionary[self.dtype])
                    return dictionary[self.dtype]
                else:
                    #print(self.dtype)
                    return np.nan
            #df['x'] = filtered.value.map(lambda val: val[self.dtype])

            if False:
                setMissing = set()
                setFound = set()
                for x in filtered.value:
                    if self.dtype not in x:
                        setFound.add(','.join(list(x.keys())))
                    else:
                        setMissing.add(','.join(list(x.keys())))
                print('setFound =                                 ', setFound)
                print('setMissing = ', setMissing)

            df['x'] = filtered.value.map(GetValue)
            # df['x'] = filtered.value
            self.used_sources[sens] = ColumnDataSource(data=df)
            self.sources[sens] = ColumnDataSource(data=df)

            # This is a dumb workaround I found to get bokeh to let me toggle plots. It basically just creates a
            # ColumnDataSource of NaNs and plots that.
            z = np.empty(len(self.sources[sens].data['x'])) * np.nan
            self.null_sources[sens] = ColumnDataSource(data=dict(x=z, t=z))

    def make_plot(self):
        """
        makes initial bokeh plots of all data in sources.
        """
        colors = Spectral11
        for i, sens in enumerate(self.sensor_names):
            # print(self.used_sources[sens].data['t'])
            self.plot.circle(x='t', y='x', source=self.used_sources[sens], color=colors[i], legend=sens)

    def update_plot(self, new):
        """
        Bokeh callback that updates this DataSet's plots.
        """
        active_sens = [self.sensor_names[ind] for ind in self.cbg.active]
        print(active_sens)
        for sens in self.sensor_names:

            if sens in active_sens:
                print(sens + ' is on')
                self.used_sources[sens].data.update(self.sources[sens].data)
            else:
                print(sens + ' is off')
                self.used_sources[sens].data.update(self.null_sources[sens].data)


# All data is initially stored as a string, so this function converts anything that needs to be a numeric.
def format_data(key, val):
    """
    :param key: str
    :param val: str
    :return: either string or float

    Since most of our data is numeric with a few things reporting strings, we need to selective convert the data depending on
    the requisite type. 
    Data will be converted to a float if it can.  
    Otherwise it will be converted to a string.
    """
    try:
        result = float(val)
    except:
        result = val.replace(',', ';')
    return result


# Process sensor values to give them dict format
def dictify(string):
    """
    :param string: str
    :param string_data: str
    :return: dict

    This function evaluates a string containing a dictionary and converts it to a true dictionary type.
    """
    d = dict(v.split(':') for v in eval(string))
    d = {k: format_data(k, d[k]) for k in d.keys()}
    return d


def load_params():
    #data = pd.read_json('./waggle_dash/testdata.json')
    #data.rename(columns={'node_id': 'id', 'timestamp': 'time', 'data': 'value'}, inplace=True)

    params = json.load(open('./waggle_sensors.json'))
    sensor_names = {}
    for p in params:
        k = p['parameter']
        if k in sensor_names:
            sensor_names[k].append(p['sensor'])
        else:
            sensor_names[k] = [p['sensor']]

    data_types = list(sensor_names.keys())
    return sensor_names, data_types

def compute_params(data):
    #data = pd.read_json('./waggle_dash/testdata.json')
    #data.rename(columns={'node_id': 'id', 'timestamp': 'time', 'data': 'value'}, inplace=True)

    sensor_names = {}
    for idxRow, row in data.iterrows():
        sensor = row['sensor']
        params  = row['value'].keys()
        for param in params:
            if param in sensor_names:
                if sensor not in sensor_names[param]:
                    sensor_names[param].append(sensor)
            else:
                sensor_names[param] = [sensor]
    data_types = sorted(sensor_names.keys())
    return sensor_names, data_types


def load_data(node_ids, dates):
    """
    :param node_ids: [str]
    :param date: str
    :return: pd.DataFrame()

    Take in a list of nodes and a date and returns a data frame that has all the data from those nodes on that date as a
    concatenated data frame. This data frame will be used to populate the specific DataSet classes. In the future it may
    be worth getting rid of this and having each DataSet instance fetch its own data.
    """
    print(node_ids)
    rdelim = '\n'  # row delimiter
    cdelim = ';'  # column delimiter
    data = pd.DataFrame()
    for date in dates:
        for node_id in node_ids:
            print(node_id)
            print(date)
            req = requests.get('http://beehive1.mcs.anl.gov/api/1/nodes/' + node_id + '/export?date=' + date)
            content = str(req.content, 'utf-8')
            # print(content)
            content = content.split(rdelim)

            # id, date, time, sensor, value, time is a datetime,
            labels = ['id', 'date', 'module', 'num', 'type', 'time', 'sensor', 'file', 'value']
            string_data = ['MAC Address', 'data', 'config', 'firmware']

            df = pd.DataFrame([row.split(cdelim) for row in content], columns=labels)
            df = df.iloc[:-2]  # The last two lines are not actually data
            if True:
                df.value = df.value.apply(dictify)
            else:
                for row in df.value:
                    setMissing = set()
                    setFound = set()
                    for x in filtered.value:
                        if self.dtype not in x:
                            setFound.add(self.dtype)
                        else:
                            setMissing.add(self.dtype)
                    print('setFound = ', setFound)
                    print('setMissing = ', setMissing)


            df['relative_time'] = df.time.apply(time_to_float)
            df.time = df.time.apply(pd.to_datetime)
            data = data.append(df, ignore_index=True)

    return data


def time_to_float(time, tz_shift=-5):
    """
    :param time: str
    :param tz_shift: float
    :return: float

    This function takes a time in the format hour,minute,second and convert it to a float between 0 and 24. Because
    times are reported in UTC, we allow for a time zone shift so it is easier to visualize the data in local time.
    """
    # split time string
    t = time.split()[1].split(sep=':')
    # convert UTC time to float in hours, shift adjust for time zone
    t = (float(t[0]) + float(t[1]) / 60 + float(t[2]) / (60 ** 2) + tz_shift)
    return t


def init_panels(data, sensor_names, data_types, dates, node_id):
    data_sets = {dtype: DataSet(node_id, dtype, sensor_names[dtype], dates) for dtype in data_types}
    panels = {}
    for dset in data_sets.values():
        dset.get_sources(data)
        dset.make_plot()
        dset.cbg.on_click(dset.update_plot)
        panels[dset.dtype] = Panel(child=column([dset.wb, dset.plot]), title=dset.dtype)
    return panels

def store_csv(d, filename):
    print('Writing data to CSV file: {} ...'.format(filename))
    with open(filename, 'w') as fOut:

        # write header
        fOut.write('node_id,ingest_id,meta_id,timestamp,data_set,sensor,parameter,value,unit\n')

        # write every row of data
        # labels = ['id', 'date', 'module', 'num', 'type', 'time', 'sensor', 'file', 'value']
        for index, row in d.iterrows():
            dictValues = row['value']       # dictionary of sensor data (parameter : value)
            for k in dictValues.keys():     # output 1 line per value

                fOut.write('{},{},{},{},{},{},{},{},{}\n'.format(
                    row['id'], 0, 0, row['time'], 0, row['sensor'], k, dictValues[k], 'unit'))

def main():
    # example input:
    # bokeh serve
    # python3 waggle_dash/main.py --date 2016-07-29 --id ub_3 ub_4
    parser = argparse.ArgumentParser(description='Plot Beehive data using Bokeh')
    parser.add_argument('-dates', metavar='dates', type=str, nargs='+',
                        help='The datesa for which the data will be retrieved')
    parser.add_argument('-id', metavar='id', type=str, nargs='+',
                        help='The node IDs')
    parser.add_argument('-csv_out', type=str, nargs='?',
                        help='the csv file to which the data is saved.')
    args = parser.parse_args()
    # node_ids = {'ub_1': '0000001e06107d6b',
    #             'ub_2': '0000001e06107e4c',
    #             'ub_3': '0000001e06107d7f',
    #             'ub_4': '0000001e06107cc5'
    #             # 'ub_5':'0000001e06107cdc'
    #             }
    print(args)
    #nodes = {'ub_3': '0000001e06107d7f', 'ub_4': '0000001e06107cc5'}
    dates = args.dates  # '2016-07-29'
    node_ids = args.id
    print(dates)
    data = load_data(node_ids, dates)
    if (args.csv_out):
        store_csv(data, args.csv_out)
    else:
        sensor_names, data_types = compute_params(data)
        if False:
            sensor_names = {'Temperature': ['TSYS01', 'TMP112', 'BMP180', 'TMP421', 'HIH6130', 'HTU21D'],
                            'Humidity': ['HTU21D', 'HIH6130'],
                            'Concentration': ['Nitrogen Di-oxide (NO2)', 'Carbon Monoxide (C0)','Hydrogen Sulphide (H2S)',
                                              'Sulfur Dioxide (SO2)']}
            data_types = ['Temperature', 'Humidity', 'Concentration']

            # sensor_names = {'Temperature': ['TSYS01']}
            # data_types = ['Temperature']
        panels = init_panels(data, sensor_names, data_types, dates, node_ids[0])
        tabs = Tabs(tabs=[panels[dtype] for dtype in data_types])

        #panels4 = init_panels(data, sensor_names, data_types, dates, node_ids['ub_4'])
        #tabs4 = Tabs(tabs=[panels4[dtype] for dtype in data_types])

        # lo = layout([[tabs4]], sizing_mode='stretch_both')

        #lo = layout(tabs, sizing_mode='stretch_both')
        session = push_session(curdoc())
        curdoc().add_root(tabs)
        session.show(tabs)
        session.loop_until_closed()

if __name__ == "__main__":
    main()

