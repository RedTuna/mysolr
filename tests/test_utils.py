# -*- coding: utf-8 -*-
import unittest

from datetime import datetime
from mysolr import to_ISO8601


class UtilsTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def test_to_ISO8601(self):
        solr_date = to_ISO8601(datetime(2014, 5, 5))
        self.assertEqual(solr_date, '2014-05-05T00:00:00Z')

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()