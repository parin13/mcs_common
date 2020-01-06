__author__ = 'parin'

from pymongo import MongoClient
import sys
from mcs_common import common_ut as common_util

class CreateDbConnection:
    def __init__(self, logger, host, port, db_name):
        self.logger = logger
        self.host = host
        self.port = port
        self.db_name = db_name

    def init(self):
        """
        mongo db connection
        :param logger
        :return : mongo db connection
        """
        try:
            conn = MongoClient(host=self.host, port=int(self.port))
            db_name = self.db_name
            db=conn.db_name
            print("Mongo db Connected :: dbName : " + db_name)
            return db
        except Exception as e:
            error = common_util.get_error_traceback(sys, e)
            self.logger.error_logger("mongo_db_connection : %s" % error)
            raise



# def connectDatabase(dbName):
#     try:
#         conn = MongoClient(host='127.0.0.1', port=27017)
#         print("Mongo db Connected :: dbName : " + dbName)
#         return conn.fintech
#     except Exception as e:
#         print ("Error in mongo connection: " + e)
