#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import mcs_common


class UnitTests(unittest.TestCase):
    def test_import(self):
        self.assertIsNotNone(mcs_common)

    def test_project(self):
        self.assertTrue(False, "write more tests here")