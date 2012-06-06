#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
from mysolr import SolrResponse
from os.path import join, dirname
import requests
import sys
import json

class QueryTestCase(unittest.TestCase):

    def setUp(self):
        mock_file = join(dirname(__file__), 'mocks/query')
        with open(mock_file) as f:
            raw_content = None
            if sys.version_info[0] == 3 and sys.version_info[1] == 2:
                raw_content = json.dumps(eval(f.read())).encode('utf-8')
            else:
                raw_content = f.read()
            self.solr_response = SolrResponse()
            self.solr_response.raw_content = raw_content
            self.solr_response.status = 200
            self.solr_response.parse_content()

    def tearDown(self):
        pass

    def test_raw_content(self):
        self.assertNotEqual(self.solr_response.raw_content, None)

    def test_status(self):
        self.assertNotEqual(self.solr_response.solr_status, None)
        self.assertEqual(self.solr_response.solr_status, 0)

    def test_qtime(self):
        self.assertNotEqual(self.solr_response.qtime, None)
        self.assertEqual(self.solr_response.qtime, 101)

    def test_total_results(self):
        self.assertNotEqual(self.solr_response.total_results, None)
        self.assertEqual(self.solr_response.total_results, 2)

    def test_start(self):
        self.assertNotEqual(self.solr_response.start, None)
        self.assertEqual(self.solr_response.start, 0)

    def test_documents(self):
        self.assertNotEqual(self.solr_response.documents, None)
        self.assertEqual(len(self.solr_response.documents), 2)

    def test_facets(self):
        self.assertNotEqual(self.solr_response.facets, None)

if __name__ == '__main__':
    unittest.main()
