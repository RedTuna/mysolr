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
        #: Solr query URL
        self.url = None
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
        #: Facets parsed as a dict.
        self.facets = None
        if 'facet_counts' in solr_response:
            self.facets = parse_facets(solr_response['facet_counts'])
        #: Shorcut to stats resuts
        self.stats = None
        if 'stats' in solr_response:
            self.stats = solr_response['stats']['stats_fields']
        #: Spellcheck result parsed into a more readable object.
        self.spellcheck = None
        if 'spellcheck' in solr_response:
            suggestions = solr_response['spellcheck']['suggestions']
            self.spellcheck = parse_spellcheck(suggestions)
        #: Shorcut to highlighting result
        self.highlighting = None
        if 'highlighting' in solr_response:
            self.highlighting = solr_response['highlighting']

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


def parse_spellcheck(solr_suggestions):
    """ Parse spellcheck result into a more readable format. """
    result = {}
    suggestions = {}

    for i in xrange(0, len(solr_suggestions), 2):
        key = solr_suggestions[i]
        value = solr_suggestions[i+1]
        if isinstance(value, dict):
            # it's a suggestion
            suggestions[key] = value
        else:
            # it's information about spellchecking result
            result[key] = value

    result['suggestions'] = suggestions
    return result