#!/usr/bin/env python
# ANL:waggle-license
#  This file is part of the Waggle Platform.  Please see the file
#  LICENSE.waggle.txt for the legal details of the copyright and software
#  license.  For more details on the Waggle project, visit:
#           http://www.wa8.gl
# ANL:waggle-license
import web
import os
import os.path
import subprocess
import threading
import re
import sys
import logging
import pprint
import time
import hashlib
from os import listdir
from os.path import isdir, join
from mysql import Mysql
import json
import requests

# uses web.py
# see https://webpy.org/


# TODO we will need to check how long a certificate is valid, here is a code example:
#    pip install pyopenssl
#    import OpenSSL
#    import ssl, socket
#    cert=ssl.get_server_certificate(('www.google.com', 443))
#    x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
#    x509.get_notAfter()


formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - line=%(lineno)d - %(message)s')

handler = logging.StreamHandler(stream=sys.stdout)
handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


mysql_host = os.environ.get('MYSQL_HOST', 'beehive-mysql')
mysql_user = os.environ['MYSQL_USER']
mysql_passwd = os.environ['MYSQL_PASSWD']
mysql_db = os.environ['MYSQL_DB']
RABBITMQ_ADMIN_PASSWORD = os.environ['RABBITMQ_ADMIN_PASSWORD']


httpserver_port = 80

resource_lock = threading.RLock()

script_path = '/usr/lib/waggle/beehive-server/beehive-cert/SSL/'
ssl_dir = '/usr/lib/waggle/SSL/'
ssl_nodes_dir = os.path.join(ssl_dir, 'nodes')
os.makedirs(ssl_nodes_dir, exist_ok=True)

authorized_keys_file = os.path.join(ssl_nodes_dir, 'authorized_keys')

db = None


def read_file(path):
    with open(path, 'r') as file:
        return file.read().strip()


urls = (
    '/certca', 'certca',  # kept for backwards compatibility...
    '/cacert', 'certca',  # ...but this should be the actual name
    '/node/?', 'newnode',
    '/', 'index'
)

app = web.application(urls, globals())


class index:

    def GET(self):
        return 'This is the Waggle certificate server.'


class certca:

    def GET(self):
        try:
            cacert = read_file(os.path.join(ssl_dir, 'waggleca/cacert.pem'))
        except FileNotFoundError:
            return 'error: cacert file not found !?'
        return cacert


def validate_query_string(s):
    return s.startswith('?')


def validate_node_id_string(s):
    return re.match('[0-9a-fA-F]{16}$', s) is not None


def generate_token_from_key_and_cert(key, cert):
    data = (key.strip() + cert.strip()).encode()
    hexdigest = hashlib.sha1(data).hexdigest()
    return hexdigest[:8]


def generate_credentials(db, nodeid):

    node_dir = os.path.join(ssl_nodes_dir, 'node_' + nodeid)

    ##### Got node_id #####
    logger.info('GET newnode - Generating credentials for "{}".'.format(nodeid))

    rsa_public_key_file = os.path.join(node_dir, 'key_rsa.pub')
    rsa_private_key_file = os.path.join(node_dir, 'key.pem')
    signed_client_certificate_file = os.path.join(node_dir, 'cert.pem')

    rsa_public_key = ""

    with resource_lock:
        return_value = subprocess.call([
            os.path.join(script_path, 'create_client_cert.sh'),
            'node-{}'.format(nodeid.lower()),
            # BUG create_client_cert.sh already prefixes path...
            os.path.join('nodes/', 'node_' + nodeid),
        ])
        if return_value != 0:
            raise Exception("create_client_cert.sh failed")

        rsa_public_key = read_file(rsa_public_key_file)
        append_to_authorized_keys_file(rsa_public_key)

    rsa_private_key = read_file(rsa_private_key_file)
    signed_client_certificate = read_file(signed_client_certificate_file)
    #rsa_public_key = read_file(rsa_public_key_file)

    #token = generate_token_from_key_and_cert(key=rsa_private_key, cert=signed_client_certificate)

    # TODO: decide if we keep token

    db.save_node_credentials(nodeid, rsa_private_key,
                             rsa_public_key, signed_client_certificate)

    # note: do not return credentials here, use get_node_crednetials function
    return


def get_rabbitmq_username_for_nodeid(nodeid):
    nodeid = nodeid.rjust(16, '0')
    nodeid = nodeid.lower()
    return f'node-{nodeid}'


class newnode:

    def GET(self):
        query = web.ctx.query

        if not validate_query_string(query):
            logger.info('GET newnode - Invalid query string "%s"', query)
            return 'error: Invalid query string "{}".\n'.format(query)

        nodeid = query.lstrip('?').upper()

        if not validate_node_id_string(nodeid):
            logger.error('GET newnode - Invalid node ID string "%s".', nodeid)
            return 'error: Invalid node ID string "{}".\n'.format(nodeid)

        logger.info('GET newnode - Preparing to register "%s".', nodeid)

        logger.info("connecting to {} {}".format(mysql_host, mysql_db))
        # check if credentials are already in database
        db = Mysql(host=mysql_host,
                   user=mysql_user,
                   passwd=mysql_passwd,
                   db=mysql_db)

        node_credentials = db.get_node_credentials(nodeid)
        #print("node_credentials:", node_credentials, flush=True)
        if not node_credentials:
            try:
                generate_credentials(db, nodeid)
            except Exception as e:
                return "error: {}".format(str(e))

            try:
                node_credentials = db.get_node_credentials(nodeid)
            except Exception as e:
                return "error: {}".format(str(e))

        if not node_credentials:
            return "error: Could not create crdentials"

        mysql_row_node = db.get_node(nodeid)

        if not mysql_row_node:
            port = db.createNewNode(nodeid)
            if not port:
                print("Error: Node creation failed")
                raise Exception("Node creation failed")
            mysql_row_node = db.get_node(nodeid)

        port = int(db.find_port(nodeid))

        if not port:
            logger.error("Error: port number not found !?")
            raise Exception("port number not found !?")

        #print("A", flush=True)
        #print("node_credentials", node_credentials, flush=True)
        try:
            rsa_private_key = node_credentials['rsa_private_key']
            rsa_public_key = node_credentials['rsa_public_key']
            signed_client_certificate = node_credentials['signed_client_certificate']
        except Exception as e:
            return 'error: credential incomplete'
        #print("rsa_private_key:", len(rsa_private_key), flush=True)
        #print("rsa_public_key:", len(rsa_public_key), flush=True)
        #print("signed_client_certificate:", len(signed_client_certificate), flush=True)

        # add user to rabbitmq here!

        #print("port", port, flush=True)

        # print("B", '{key}\n{cert}\nPORT={ssh_port}'.format(
        #    key=rsa_private_key, cert=signed_client_certificate, ssh_port=port) , flush=True)
        # removed TOKEN={token}\n
        return_content = '{key}\n{cert}\nPORT={ssh_port}\n{ssh_key}\n'.format(
            key=rsa_private_key,
            cert=signed_client_certificate,
            ssh_port=port,
            ssh_key=rsa_public_key)

        username = get_rabbitmq_username_for_nodeid(nodeid)
        logger.info('updating username %s in rabbitmq', username)

        with requests.Session() as session:
            # TODO need to user correct admin password, or add user for local work
            session.auth = ('admin', RABBITMQ_ADMIN_PASSWORD)
            # TODO allow us to verify server certificate (or user http)
            session.verify = False

            session.put(f'https://beehive-rabbitmq:15671/api/users/{username}', json={
                'password_hash': '',  # disable password based login
                'tags': '',
            })

            session.put(f'https://beehive-rabbitmq:15671/api/permissions/%2f/{username}', json={
                'configure': '^to-{}$'.format(username),
                'write': '^messages|data-pipeline-in|logs|images$',
                'read': '^to-{}$'.format(username),
            })

        return return_content


def update_authorized_keys_file():
    pass


def append_to_authorized_keys_file(data):
    with open(authorized_keys_file, 'a') as file:
        file.write(data.strip())
        file.write('\n')

    os.chmod(authorized_keys_file, 0o600)


if __name__ == "__main__":
    node_database = {}

    print("mysql_host={}".format(mysql_host), flush=True)
    print("mysql_db={}".format(mysql_db), flush=True)
    print("mysql_user={}".format(mysql_user), flush=True)

    # get all public keys from disk
    for directory in listdir(ssl_nodes_dir):
        node_dir = join(ssl_nodes_dir, directory)
        if isdir(node_dir) and directory[0:5] == 'node_':
            rsa_pub_filename = os.path.join(node_dir, 'key_rsa.pub')
            try:
                with open(rsa_pub_filename, 'r') as rsa_pub_file:
                    data = rsa_pub_file.read()
                    node_id = directory[5:].upper()
                    node_database[node_id] = {}
                    node_database[node_id]['pub'] = data
            except Exception as e:
                logger.error("Error reading file %s: %s" %
                             (rsa_pub_filename, str(e)))

    print("node_database: (public keys only)", flush=True)
    print(str(node_database), flush=True)

    db = Mysql(host=mysql_host,
               user=mysql_user,
               passwd=mysql_passwd,
               db=mysql_db)

    while True:
        try:
            for row in db.query_all('SHOW TABLES'):
                print("table:", row, flush=True)
        except Exception as e:
            print("got exception: ", str(e), flush=True)
            print("waiting 3 seconds for another connection test...", flush=True)
            time.sleep(3)
            continue
        break

    # get list of nodes with credentials in MySQL
    credentials_in_mysql = {}
    for row in db.query_all('SELECT node_id FROM credentials'):
        print(row, flush=True)
        node_id = row[0]
        credentials_in_mysql[node_id] = {'node_id': node_id}

    # load credentials into MySQL (only used temporarily to move files into mysql)
    for d in listdir(ssl_nodes_dir):
        node_dir = join(ssl_nodes_dir, d)
        if isdir(node_dir) and d[0:5] == 'node_':
            node_id = d[5:].upper()
            if node_id in credentials_in_mysql:
                print("good, already in database", flush=True)
            else:
                print(
                    "credentials missing in db! Trying to load into MYSQL ...", flush=True)

                rsa_public_key_file = os.path.join(node_dir, 'key_rsa.pub')
                rsa_private_key_file = os.path.join(node_dir, 'key.pem')
                signed_client_certificate_file = os.path.join(
                    node_dir, 'cert.pem')

                try:
                    rsa_private_key = read_file(rsa_private_key_file)
                    rsa_public_key = read_file(rsa_public_key_file)
                    signed_client_certificate = read_file(
                        signed_client_certificate_file)
                except OSError as e:
                    sys.exit('Could not read credential files: {}'.format(str(e)))

                try:
                    db.save_node_credentials(
                        node_id, rsa_private_key, rsa_public_key, signed_client_certificate)
                except Exception as e:
                    sys.exit(
                        'Could not save credentials to MySQL database: {}'.format(str(e)))

    # get port: for node_id SELECT reverse_ssh_port FROM nodes WHERE node_id='0000001e06200335';
    # get nodes and ports from database
    for row in db.query_all('SELECT node_id, reverse_ssh_port FROM nodes'):
        print(row, flush=True)

        node_id = row[0].upper()

        if not node_id in node_database:
            logger.warning(
                "Node %s is in database, but no public key was found")
            node_database[node_id] = {}

        try:
            port = int(row[1])
        except:
            port = None

        if port:
            node_database[node_id]['reverse_ssh_port'] = port
        else:
            logger.warning("node %s has no port assigned" % (node_id))

    # explicit check for consistency
    for node_id in node_database:
        #logger.debug("node_id: %s" % (node_id))
        if not 'reverse_ssh_port' in node_database[node_id]:
            logger.warning(
                "Node %s has public key, but no port number is assigned in database." % (node_id))

    print("node_database:", flush=True)
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(node_database)

    # TODO Support multiple auth keys here. We can keep them in a directory or
    # the database.

    auth_options = 'no-X11-forwarding,no-agent-forwarding,no-pty'
    registration_script =\
        '/usr/lib/waggle/beehive-server/beehive-sshd/register.sh'
    registration_key_filename =\
        '/usr/lib/waggle/ssh_keys/id_rsa_waggle_aot_registration.pub'
    with open(registration_key_filename) as registration_key_file:
        registration_key = registration_key_file.readline().strip()
    new_authorized_keys_content = ['command="%s",%s %s\n'
                                   % (registration_script, auth_options, registration_key)]

    for node_id in node_database.keys():
        line = None

        if 'pub' in node_database[node_id]:
            if 'reverse_ssh_port' in node_database[node_id]:
                port = node_database[node_id]['reverse_ssh_port']
                permitopen = 'permitopen="localhost:%d"' % (port)
                line = "%s,%s %s node:%s\n" % (
                    permitopen, auth_options, node_database[node_id]['pub'].strip(), node_id)
            else:

                logger.warning("Node %s has no reverse_ssh_port" % (node_id))
                # add public keys without port number, but comment the line
                permitopen = 'permitopen="localhost:?"'
                line = "#%s,%s %s node:%s\n" % (
                    permitopen, auth_options, node_database[node_id]['pub'].strip(), node_id)
        else:
            logger.warning("Node %s has no public key" % (node_id))

        if line:
            logger.debug(line)
            new_authorized_keys_content.append(line)

    # create new authorized_keys file on every start, just to be sure.
    with open(authorized_keys_file, 'w') as file:
        file.writelines(new_authorized_keys_content)

    os.chmod(authorized_keys_file, 0o600)

    web.config.debug = False
    web.httpserver.runsimple(app.wsgifunc(), ("0.0.0.0", httpserver_port))
    app.run()
