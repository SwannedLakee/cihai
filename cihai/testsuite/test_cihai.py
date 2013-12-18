# -*- coding: utf-8 -*-
"""Tests for cihai.

cihai.testsuite.test_unihan
~~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: Copyright 2013 Tony Narlock.
:license: BSD, see LICENSE for details

"""

from __future__ import absolute_import, division, print_function, \
    with_statement, unicode_literals

import os
import sys
import re
import tempfile
import random
import logging

import sqlalchemy

from .. import conversion

from .helpers import unittest, CihaiTestCase
from .._compat import PY2, text_type
from ..cihai import Cihai, NoDatasets
from ..util import get_datafile

log = logging.getLogger(__name__)


def add_to_path(path):
    """Adds an entry to sys.path if it's not already there.  This does
    not append it but moves it to the front so that we can be sure it
    is loaded.
    """
    if not os.path.isdir(path):
        raise RuntimeError('Tried to add nonexisting path')

    def _samefile(x, y):
        if x == y:
            return True
        try:
            return os.path.samefile(x, y)
        except (IOError, OSError, AttributeError, TypeError):
            # Windows has no samefile
            return False
    sys.path[:] = [y for y in sys.path if not _samefile(path, y)]
    sys.path.insert(0, path)


add_to_path(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'test_middleware'))
)
from simple import DatasetExample


class CihaiInstance(CihaiTestCase):

    def test_no_datasets(self):
        c = Cihai()
        self.assertIsInstance(c, Cihai)

        with self.assertRaises(NoDatasets) as e:
            c = c.get('好')

        with self.assertRaises(NoDatasets) as e:
            c = c.reverse('好')

        self.assertIsInstance(c.metadata, sqlalchemy.MetaData)
        self.assertIsInstance(c._metadata, sqlalchemy.MetaData)
        self.assertIsInstance(c._metadata.bind, sqlalchemy.engine.Engine)


class CihaiDatabaseInstance(CihaiTestCase):

    # :todo: change this to create/drop table for class.

    def setUp(self):
        super(CihaiDatabaseInstance, self).setUp()

        self.tables = self.c.metadata.tables

    def test_table_exists(self):

        if not self.tables:
            self.skipTest('No tables to test.')

        table = self.c.get_table(random.choice(list(self.tables)))
        self.assertIsInstance(table, sqlalchemy.Table)

        for table_name in self.tables:
            self.assertTrue(self.c.table_exists(table_name))
            self.assertIsInstance(table_name, text_type)

    def test_get_table(self):
        # pick a random table name.

        if not self.tables:
            self.skipTest('No tables to test.')

        table = self.c.get_table(random.choice(list(self.tables)))
        self.assertIsInstance(table, sqlalchemy.Table)


class CihaiMiddleware(unittest.TestCase):

    def test_add_middleware(self):
        """asdf."""
        c = Cihai()

        self.assertFalse(c._middleware, msg="Has no middleware at start.")

        c.use(DatasetExample)

        for m in c._middleware:
            self.assertIsInstance(m, DatasetExample)

        with self.assertRaisesRegexp(Exception, 'Dataset already added.'):
            c.use(DatasetExample)

    def test_get(self):
        c = Cihai()

        with self.assertRaises(NoDatasets):
            c.get('好')

        c.use(DatasetExample)
        self.assertDictContainsSubset({
            'definition': 'ni hao'
        }, c.reverse('ni hao'))

    def test_reverse(self):
        c = Cihai()

        with self.assertRaises(NoDatasets):
            c.reverse('ni hao')

        c.use(DatasetExample)
        self.assertDictContainsSubset({
            'definition': 'ni hao'
        }, c.reverse('ni hao'))


class UtilTest(unittest.TestCase):

    def test_get_datafile(self):
        data_filename = 'data.ext'

        data_abspath = get_datafile(data_filename)
        self.assertNotEqual(data_filename, data_abspath)
        self.assertIsInstance(data_abspath, text_type)