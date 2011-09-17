# -*- coding: utf-8 -*-
""" SolrResponse class that provides an easy access to a solr search
response.

>>> response.status
0
>>> response.total_result
10
>>> reponse['qtime']
13

"""


class SolrResponse(object):
    """ Parse solr response and make it accesible."""

    def __init__(self, solr_response):
        """ Init method

        Arguments:
        solr_response -- Python object result of search query

        """
        #: Solr full response.
        self.raw_response = solr_response
        #: Response status.
        self.status = solr_response['responseHeader']['status']
        #: Query time.
        self.qtime = solr_response['responseHeader']['QTime']
        #: Number of results.
        self.total_results = solr_response['response']['numFound']
        #: Offset.
        self.start = solr_response['response']['start']
        #: Documents list.
        self.documents = solr_response['response']['docs']
        if 'facet_counts' in solr_response:
            #: Facets parsed as a dict.
            self.facets = parse_facets(solr_response['facet_counts'])

    def __repr__(self):
        values = (self.status, self.qtime, self.total_results)
        return '<SolrResponse status=%d, qtime=%d, total_results=%d>' % values


def parse_facets(solr_facets):
    """ Parse facets."""
    result = {}
    for facet_type, facets in solr_facets.iteritems():
        facet_type_dict = {}
        for name, facet in facets.iteritems():
            parsed = [tuple(facet[i:i+2]) for i in xrange(0, len(facet), 2)]
            facet_type_dict[name] = dict(parsed)
        result[facet_type] = facet_type_dict
    return result
