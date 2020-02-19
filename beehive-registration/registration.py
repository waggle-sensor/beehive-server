#!/usr/bin/env python3
import logging
import os.path
import re
import sys
import json
import time
import requests
#from export import export_generator, list_node_dates, get_nodes_last_update_dict
# sys.path.append("..")
#from waggle_protocol.utilities.mysql import *
from flask import Flask
from flask import Response
from flask import request
from flask import jsonify
from flask import stream_with_context
#import mysqlclient
#from MySQLdb import _mysql
import MySQLdb as _mysql
import uuid
from werkzeug.exceptions import HTTPException


app = Flask(__name__)
# app.logger.setLevel(logging.INFO)

logger = logging.getLogger('beehive-api')
logger.setLevel(logging.INFO)

#handler = JournalHandler()
# handler.setLevel(logging.INFO)
# logger.addHandler(handler)
# app.logger.addHandler(handler)

# Publish errors to Slack.
#handler = SlackHandler('https://hooks.slack.com/services/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')
# handler.setLevel(logging.ERROR)
# logger.addHandler(handler)
# app.logger.addHandler(handler)

port = 80
api_url_internal = 'http://localhost'
api_url = 'http://beehive1.mcs.anl.gov'

# modify /etc/hosts/: 127.0.0.1	localhost beehive1.mcs.anl.gov
STATUS_Bad_Request = 400  # A client error
STATUS_Unauthorized = 401
STATUS_Not_Found = 404
STATUS_Server_Error = 500

ALWAYS_APPROVE = (os.environ.get('ALWAYS_APPROVE') == '1')

# class InvalidUsage(Exception):
#     status_code = 400

#     def __init__(self, message, status_code=None, payload=None):
#         Exception.__init__(self)
#         self.message = message
#         if status_code and status_code==STATUS_Server_Error:
#             logger.warning(message)
#         else:
#             logger.debug(message)
#         if status_code is not None:
#             self.status_code = status_code
#         self.payload = payload

#     def to_dict(self):
#         rv = dict(self.payload or ())
#         rv['message'] = self.message
#         return rv


# @app.errorhandler(InvalidUsage)
# def handle_invalid_usage(error):
#    response = jsonify(error.to_dict())
#    response.status_code = error.status_code
#    return response


@app.errorhandler(Exception)
def handle_error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    return jsonify(error=str(e)), code


def get_mysql_db():
    host = os.environ.get("MYSQL_HOST")
    user = os.environ.get("MYSQL_USER")
    passwd = os.environ.get("MYSQL_PASSWD")
    db = os.environ.get("MYSQL_DB")

    return _mysql.connect(host=host, user=user, passwd=passwd, db=db)


# create registration request
# POST /api/registration?nodeid=<id>
# return request id

# check on registration request
# GET /api/registration/<id>
# returns "waiting for approval", "request denied", "success: <stuff>"
# successful  request has to expire in 5 minutes !?


# UPDATE registrations SET state='denied' , response_date=NOW() WHERE id='';
# UPDATE registrations SET state='approved' , response_date=NOW() WHERE id='';

def execute(query):

    db = get_mysql_db()
    c = db.cursor()

    try:
        c.execute(query)

        db.commit()

    # except _mysql.Error as e:
    except Exception as e:

        # except MySQLdb.Error as e: #MySQLdb.Warning
        try:
            error_message = "MySQL Error [{}]: {}".format(e.args[0], e.args[1])
            print(error_message, flush=True)
            e = Exception(error_message)
            raise e
            #return_obj['error'] = error_message
            # return jsonify(return_obj), STATUS_Server_Error
        except IndexError:
            error_message = "MySQL Error: {}".format(str(e))
            print(error_message, flush=True)
            # print(error_message)
            e = Exception(error_message)
            raise e
            #return_obj['error'] = error_message
            # return jsonify(return_obj), STATUS_Server_Error

    return


def valid_nodeid(s):
    return re.match(r'[A-Fa-f0-9]{16}', s) is not None


def create_registration_request(nodeid):

    print("create_registration_request", flush=True)

    if not valid_nodeid(nodeid):
        raise Exception('nodeid not valid')

    registration_uuid = uuid.uuid4()

    query = "INSERT INTO registrations(id, nodeid, creation_date)  VALUES ('{}', '{}', NOW());".format(
        registration_uuid, nodeid)

    logger.debug(' query = ' + query)
    print("query:", query,  flush=True)

    return_registration_uuid = 'error'

    try:
        execute(query)
    except Exception as e:
        raise Exception("execute(query) returned: {}".format(str(e)))

    return_registration_uuid = registration_uuid

    return return_registration_uuid


@app.route('/', defaults={'request_id': None},  methods=['POST'])
def api_registration_request(request_id):

    return_obj = {}

    nodeid = request.args.get('nodeid')

    if not nodeid:
        return_obj['error'] = "Query parameter \"nodeid=<nodeid>\" is missing"
        return jsonify(return_obj), STATUS_Server_Error

    try:
        newRegistration = create_registration_request(nodeid)
    except Exception as e:
        return_obj['error'] = str(e)
        return jsonify(return_obj), STATUS_Server_Error

    return_obj['data'] = newRegistration

    return jsonify(return_obj)


@app.route('/<request_id>',  methods=['GET'])
def api_registration_check(request_id):

    return_obj = {}

    if not request_id:
        return_obj['error'] = "unclear instruction"
        return jsonify(return_obj)

    
    #query = "SELECT * FROM registrations WHERE id='{}';".format(request_id)
    query = "SELECT * FROM registrations WHERE id='%s';"
    query_param = (request_id,)
    print("query: ", query, request_id,  flush=True)

    row = None
    db = get_mysql_db()
    c = db.cursor()
    try:
        c.execute(query, query_param)

        row = c.fetchone()

    except Exception as e:
        return_obj['error'] = str(e)
        return jsonify(return_obj), STATUS_Server_Error

    if not row:
        return_obj['error'] = "{} not found".format(request_id)
        return jsonify(return_obj), STATUS_Not_Found

    if len(row) < 4:
        return_obj['error'] = "Could not parse table entry"
        return jsonify(return_obj), STATUS_Server_Error

    state = row[3]
    nodeid = row[1]

    if (state != 'approved') and (ALWAYS_APPROVE is False):
        print("row:", row, flush=True)
        return_obj['data'] = {}
        return_obj['data']['request_id'] = request_id
        return_obj['data']['state'] = state
        return jsonify(return_obj)

    query_url = 'http://beehive-cert:80/node?{}'.format(nodeid)
    print("query: ", query_url, flush=True)
    try:
        r = requests.get(query_url)
        r.raise_for_status()
    except Exception as e:
        return_obj['error'] = "Could not retreive credentials from cert server: {}".format(
            str(e))
        return jsonify(return_obj), STATUS_Server_Error

    return r.content


if __name__ == '__main__':
    app.run(host='0.0.0.0')
