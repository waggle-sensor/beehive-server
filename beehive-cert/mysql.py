import logging
# ANL:waggle-license
#  This file is part of the Waggle Platform.  Please see the file
#  LICENSE.waggle.txt for the legal details of the copyright and software
#  license.  For more details on the Waggle project, visit:
#           http://www.wa8.gl
# ANL:waggle-license
import MySQLdb
from contextlib import contextmanager

logging.basicConfig()
logger = logging.getLogger(__name__)


class Mysql(object):

    def __init__(self, host='localhost', user='', passwd='', db=''):
        self._host = host
        self._user = user
        self._passwd = passwd
        self._db = db

    @contextmanager
    def get_cursor(self, query):
        db = MySQLdb.connect(
            host=self._host,
            user=self._user,
            passwd=self._passwd,
            db=self._db)

        cur = db.cursor()
        logger.debug("query: " + query)
        try:
            cur.execute(query)
            db.commit()
            logger.debug("query was successful")
        except Exception as e:
            logger.error("query failed: (%s) %s" % (str(type(e)), str(e) ) )

        yield cur

        cur.close()
        db.close()

    def query_all(self, query):
        """
        MySQL query that returns multiple results in form of a generator
        """
        with self.get_cursor(query) as cur:
            # get array:
            for row in cur.fetchall():
                yield row

    def query_one(self, query):
        """
        MySQL query that returns a single row (array)
        """
        with self.get_cursor(query) as cur:
            return cur.fetchone()

    def get_node(self, node_id):
        return self.query_one("SELECT * FROM nodes WHERE node_id='{0}'".format(node_id))

    def find_port(self, node_id):
        row = self.query_one("SELECT reverse_ssh_port FROM nodes WHERE node_id='{0}'".format(node_id))

        if not row:
            logger.debug("row for %s not found" % (node_id))
            return None

        if not row[0]:
            logger.debug("row for %s does not contain port number" % (node_id))
            return None

        try:
            port = int(row[0])
        except ValueError:
            logger.error("port number %s for node %s cannot be converted" % (port, node_id))
            port = None

        return port

    def find_unused_port(self):
        # first try port = 50000
        # once port 50000 is used, find_unused_port_query can find the next unsued port number above 50000
        row = self.query_one('SELECT * FROM nodes WHERE reverse_ssh_port = 50000;')

        if row:
            # this query expects that at least one
            find_unused_port_query = """SELECT t1.reverse_ssh_port+1 AS Missing
                    FROM nodes AS t1
                    LEFT JOIN nodes AS t2 ON t1.reverse_ssh_port+1 = t2.reverse_ssh_port
                    WHERE t1.reverse_ssh_port IS NOT NULL
                        AND t2.reverse_ssh_port IS NULL
                        AND t1.reverse_ssh_port >= 50000
                    ORDER BY t1.reverse_ssh_port LIMIT 1;"""

            newport = self.query_one(find_unused_port_query)

            if not newport:
                logger.debug("newport empty")
                return newport

            try:
                newport = int(newport[0])
            except Exception as e:
                logger.error("Could not convert new port into int: %s %s %s" % (newport,str(type(e)),str(e)))
                return None

            if newport < 50000 or newport > 60000:
                logger.error("Port number %d out of range." % (newport) )
                return None
        else:
            # This most likely means that the nodes table is still empty
            newport = 50000

        logger.debug("newport: %s" % (str(newport)))
        return newport

    def createNewNode(self, node_id):
        newport = self.find_unused_port()

        if not newport:
            logger.error("createNewNode() did not get a port from find_unused_port()")
            return None

        self.query_one("INSERT INTO nodes (node_id, reverse_ssh_port) VALUES ('%s', %d)" % ( node_id, newport ))

        return newport


    def save_node_credentials(self, node_id, rsa_private_key, rsa_public_key, signed_client_certificate):
    
        query = "INSERT INTO credentials (node_id, rsa_private_key, rsa_public_key, signed_client_certificate) VALUES ('{}', '{}', '{}', '{}')".format( node_id, rsa_private_key, rsa_public_key, signed_client_certificate )
        self.query_one(query)

        return

    def get_node_credentials(self, node_id):
    
        query = "SELECT * FROM credentials WHERE node_id = '{}';".format(node_id) 
        row = self.query_one(query)

        if not row:
            return None 

        row_len  =    len(row)     
        if row_len != 5:
            raise Exception("error reading credentials {}".format(row_len))

        #print("row:", row, flush=True)
        # id, nodeid, 
        result = {
            'nodeid' : row[1],
            'rsa_private_key' : row[2] , 
            'rsa_public_key' : row[3], 
            'signed_client_certificate' : row[4],
        }
        return result



