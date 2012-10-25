# -*- coding: utf-8 -*-
import time
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

    def test_commit(self):
        response = self.solr.commit()
        self.assertEqual(response.status, 200)

    def test_optimize(self):
        response = self.solr.optimize()
        self.assertEqual(response.status, 200)

    def test_ping(self):
        response = self.solr.ping()
        self.assertEqual(response.status, 200)

    def test_is_up(self):
        response = self.solr.is_up()
        self.assertEqual(response, True)

    def test_update_delete(self):
        # Get total results
        response = self.solr.search(q='*:*')
        self.assertEqual(response.status, 200)
        total_results = response.total_results
        # Post one document using json
        documents = [{'id' : 1}]
        response = self.solr.update(documents, input_type='json')
        self.assertEqual(response.status, 200)
        # Post anoter document using xml
        documents = [{'id' : 2}]
        response = self.solr.update(documents, input_type='xml')
        self.assertEqual(response.status, 200)
        # Compare total results
        response = self.solr.search(q='*:*')
        self.assertEqual(response.status, 200)
        self.assertEqual(response.total_results, total_results + 2)

        # Now delete the two document posted above
        query = 'id:1'
        key = 2
        response = self.solr.delete_by_query(query)
        self.assertEqual(response.status, 200)
        response = self.solr.delete_by_key(key)
        self.assertEqual(response.status, 200)
        response = self.solr.search(q='*:*')
        self.assertEqual(response.status, 200)
        self.assertEqual(response.total_results, total_results)

    def tearDown(self):
        pass

    def test_query(self):
        pass

if __name__ == '__main__':
    unittest.main()
