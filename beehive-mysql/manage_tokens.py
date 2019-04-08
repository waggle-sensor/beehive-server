#!/usr/bin/env python3
# ANL:waggle-license
#  This file is part of the Waggle Platform.  Please see the file
#  LICENSE.waggle.txt for the legal details of the copyright and software
#  license.  For more details on the Waggle project, visit:
#           http://www.wa8.gl
# ANL:waggle-license
# e.g. docker exec -ti beehive-api bash
import logging
import MySQLdb
from contextlib import contextmanager
logging.basicConfig()
logger = logging.getLogger(__name__)

import uuid

@contextmanager
def get_cursor(query, params):
    # using with does not work here
    db = MySQLdb.connect(  host="beehive-mysql",    
                                 user="waggle",       
                                 passwd="waggle",
                                 db='waggle')
    cur = db.cursor()
    
    try:
        if params:
            cur.execute(query, params)
        else:
            cur.execute(query)
        
        db.commit()
        logger.debug("query was successful")
    except Exception as e:
        logger.error("query failed: (%s) %s" % (str(type(e)), str(e) ) )
    print("ok")
    yield cur
    cur.close()
    db.close()



def query_one(query, params):
        """
        MySQL query that returns a single row (array)
        """
        with get_cursor(query, params) as cur:
            return cur.fetchone()


def getToken(username):
    row = query_one('SELECT token FROM users WHERE username=%s', [username])
    return row[0]



                             
def newToken(username):
    newtoken = str(uuid.uuid4())
    sql_statement = "UPDATE users SET token='{}' WHERE username=%s".format(newtoken)
    query_one(sql_statement, [username])
                                 

token = getToken('wolfgang')
print(token)

