#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = "0.0.0.1"

from mcs_common.services import logger, mongo_db, services_mysql ,custom_exception
from . import ref_strings

import os, sys
from os.path import dirname, join, abspath

sys.path.insert(0, abspath(join(dirname(__file__), '..')))

def get_error_traceback(sys, e):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    return "%s || %s || %s || %s" %(exc_type, fname, exc_tb.tb_lineno,e)


class CommonUtil:
    def __init__(self, log, env):
        self.logger = None
        self.log = log
        self.env = env
        self.logs_directory = self.env.get(self.log, 'path')
        self.log_category = self.env.get(self.log, 'category')

    def create_logger(self):
        self.logger = logger.CreateLogger(self.logs_directory, self.log_category)


    def mysql_init(self, host, user, port, password, db_name):
        try:
            print ('inside mysql_init')
            print (host,user,port)
            db_instance = services_mysql.CreateDbConnection(self.logger, host, user, port, password, db_name)
            return db_instance
        except Exception as e:
            raise e


