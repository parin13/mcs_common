# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from mcs_common import common_ut as common_util
import MySQLdb
import os, sys


class CreateDbConnection:

    def __init__(self, logger, host, user, port, password, db_name):
        self.logger = logger
        self.host = host
        self.user = user
        self.port = port
        self.db_name = db_name
        self.password = password

    def init(self):
        """
        mongo db connection
        :param logger
        :return : mongo db connection
        """
        try:
            db = MySQLdb.connect(
                host=self.host,
                user=self.user,
                passwd=self.password,
                db=self.db_name
            )
            print("********db connection sucess*******")
            return db

        except Exception as e:
            error = common_util.get_error_traceback(sys, e)
            print (error)
            self.logger.error_logger("services mysql connection : %s" % error)
            raise e

    def find_sql(self, table_name, filters={}, columns='', sort=False):
        try:
            data = None
            db_con = self.init()
            cursor = db_con.cursor(MySQLdb.cursors.DictCursor)

            if columns:
                columns = ','.join(columns)
            else:
                columns = '*'

            if filters:
                params = query_from_filter(filters)
                query = 'SELECT %s FROM %s WHERE %s' %(columns, table_name, params)
            else:
                query = 'SELECT %s FROM %s' %(columns, table_name)

            if sort:
                query += ' ORDER BY timestamp DESC '

            cursor.execute(query)
            data = cursor.fetchall()
            self.logger.msg_logger('>>>>>>>> MYSQL Find Success : %s' %(query))

        except Exception as e:
            error = common_util.get_error_traceback(sys, e)
            self.logger.error_logger('find_sql : %s || ' % (error))
        finally:
            if db_con: db_con.close()
            return data
