# -*- coding: utf-8 -*-
import unittest


from mysolr import SolrResponse
from os.path import join, dirname


class HighlightingQueryTestCase(unittest.TestCase):
    """ """

    def setUp(self):
        mock_file = join(dirname(__file__), 'mocks/highlightingquery')
        with open(mock_file) as f:
            mock = eval(f.read())
            self.response = SolrResponse(mock)

    def tearDown(self):
        pass

    def test_query(self):
        self.assertNotEqual(self.response.highlighting, None)


if __name__ == '__main__':
    unittest.main()