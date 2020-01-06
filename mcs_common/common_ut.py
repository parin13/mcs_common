#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = "0.0.0.1"

from mcs_common.services import logger, mongo_db, custom_exception
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

    @staticmethod
    def mongo_init(log, host, port, db_name):
        try:
            db = mongo_db.CreateDbConnection(log, host, port, db_name)
            return db.init()

        except Exception as e:
            raise