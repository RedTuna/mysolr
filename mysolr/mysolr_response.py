# -*- coding: utf-8 -*-
"""
"""

class SolrDict(dict):
    """ Easy-use dictionary. """

    def __getattr__(self, key):
        """ getattr = getitem. """
        return self.__getitem__(key)

    def __setattr__(self, key, value):
        """ setattr = setitem. """
        self.__setitem__(key, value)

    def __missing__(self, key):
        """ Return None instead of KeyError. """
        return None

class SolrResponse(SolrDict):
    """ Parse solr response and make it accesible. """

    def __init__(self, solr_response):
        """ Init method
        arguments:
        solr_response -- Python object result of search query
        """
        self.status = solr_response['responseHeader']['status']
        self.qtime = solr_response['responseHeader']['QTime']
        self.total_results = solr_response['response']['numFound']
        self.start = solr_response['response']['start']
        self.documents = solr_response['response']['docs']
        self.facets = self.__parse_facets(solr_response['facet_counts'])
  
    def __parse_facets(self, solr_facets):
        """ Parse facets. """
        result = SolrDict()
        for facet_type, facets in solr_facets.iteritems():
            facet_type_dict = SolrDict()
            for name, facet in facets.iteritems():
                parsed = [tuple(facet[i:i+2]) for i in xrange(0, len(facet), 2)]
                facet_type_dict[name] = SolrDict(parsed)
            result[facet_type] = facet_type_dict
        return result