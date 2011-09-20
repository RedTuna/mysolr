#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
from mysolr import SolrResponse
from os.path import join, dirname

class QueryTestCase(unittest.TestCase):

    def setUp(self):
        mock_file = join(dirname(__file__), 'mocks/query')
        mock = eval(open(mock_file).read())
        self.solr_response = SolrResponse(mock)

    def tearDown(self):
        pass

    def test_raw_response(self):
        self.assertIsNotNone(self.solr_response.raw_response)

    def test_status(self):
        self.assertIsNotNone(self.solr_response.status)
        self.assertEqual(self.solr_response.status, 0)

    def test_qtime(self):
        self.assertIsNotNone(self.solr_response.qtime)
        self.assertEqual(self.solr_response.qtime, 101)

    def test_total_results(self):
        self.assertIsNotNone(self.solr_response.total_results)
        self.assertEqual(self.solr_response.total_results, 2)

    def test_start(self):
        self.assertIsNotNone(self.solr_response.start)
        self.assertEqual(self.solr_response.start, 0)

    def test_documents(self):
        self.assertIsNotNone(self.solr_response.documents)
        self.assertEqual(len(self.solr_response.documents), 2)

    def test_facets(self):
        self.assertIsNotNone(self.solr_response.facets)

if __name__ == '__main__':
    unittest.main()
