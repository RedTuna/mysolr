# -*- coding: utf-8 -*-
import unittest
from mysolr import Solr


class QueryResultTestCase(unittest.TestCase):

    def setUp(self):
        self.solr = Solr('http://localhost:8983/solr')

    def test_search(self):
        response = self.solr.search(q='*:*')
        self.assertEqual(response.status, 200)
        self.assertEqual(response.total_results, 4)
        self.assertEqual(len(response.documents), 4)

    def test_search_cursor(self):
        cursor = self.solr.search_cursor(q='*:*')
        i = 0
        for response in cursor.fetch(1):
            self.assertEqual(response.status, 200)
            i += 1
        self.assertEqual(i, 4)

        cursor = self.solr.search_cursor(q='*:*')
        i = 0
        for response in cursor.fetch(4):
            self.assertEqual(response.status, 200)
            i += 1
        self.assertEqual(i, 1)

    def tearDown(self):
        pass

    def test_query(self):
        pass

if __name__ == '__main__':
    unittest.main()
