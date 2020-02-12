# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from mcs_common import common_ut as common_util
import MySQLdb
import os, sys


def query_from_filter(filters, type='AND', search=False):
    params = ''

    if search:
        for key, value in filters.items():
            params += "lower({0}) LIKE '%{1}%' {2} ".format(key, value.lower(), type)
    else:
        for key, value in filters.items():
            params += "%s = '%s' %s " % (key, value, type)
    return params[:-(len(type)+2)]



def query_from_data(insert_data):
    condition = ''
    for key,value in insert_data.items():
        if type(value) == str:
            condition += "'{}'".format(value)+','
        else:
            condition += '{}'.format(value)+','

    return condition[:-1]



class CreateDbConnection:

    def __init__(self, logger, host, user, port, password, db_name):
        self.logger = logger
        self.host = host
        self.user = user
        self.port = port
        self.db_name = db_name
        self.password = password

    def init(self):
        try:
            db = MySQLdb.connect(
                host=self.host,
                user=self.user,
                passwd=self.password,
                db=self.db_name
            )
            return db

        except Exception as e:
            error = common_util.get_error_traceback(sys, e)
            print (error)
            self.logger.error_logger(" mysql init : %s" % error)
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

    def insert_sql(self, table_name, insert_data):
        try:
            data = None
            ret_status = False
            db_con = self.init()
            cursor = db_con.cursor(MySQLdb.cursors.DictCursor)
            query = 'insert into %s (%s) Values (%s)' %(table_name, ','.join([key for key in insert_data]), query_from_data(insert_data))
            print(query)
            cursor.execute(query)
            db_con.commit()
            ret_status = True
            self.logger.msg_logger('>>>>>>>> MYSQL Insert Success : %s' %(query))

        except Exception as e :
            error = common_util.get_error_traceback(sys, e)
            print (error)
            self.logger.error_logger('insert_sql() : %s' % error)
            raise e
        finally:
            if db_con: db_con.close()
            return ret_status
