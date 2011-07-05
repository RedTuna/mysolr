#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
"""

class SolrResponse(object):
    """
    """
    def __init__(self, solr_response):
        """
        """
        self.data = {}
        self.__build(solr_response)
    
    def __build(self, solr_response):
        """
        """
        self.numFound = solr_response['response']['numFound']
        self.results = solr_response['response']['docs']
        self.facet_counts = self.__build_facets(solr_response['facet_counts'])
        self.spellcheck = self.__build_spellcheck(solr_response['spellcheck'])
    
    def __build_spellcheck(self, solr_spellcheck):
        """
        """
        temp_suggestions = {}
        solr_suggestions = solr_spellcheck['suggestions']
        for i in xrange(0, len(solr_suggestions)):
            if i % 2 == 0:
                temp_suggestions[solr_suggestions[i]] = solr_suggestions[i+1]
        suggestions = {}
        suggestions['suggestions'] = temp_suggestions
        return suggestions 
  
    def __build_facets(self, solr_facets):
        """
        """
        facets = {}
        for key, values in solr_facets.items():
            facet_types = {}
            for key2, values2 in values.items():
                temp_facet = {}
                for i in xrange(0, len(values2)):
                    if i % 2 == 0:
                        temp_facet[values2[i]] = values2[i+1]
                facet_types[key2] = temp_facet
            facets[key] = facet_types
        return facets
    
    def __build_highlighting(self):
        """
        """
        raise NotImplementedError
    
    def __setitem__(self, key, value):
        """
        """
        self.data[key] = value
    
    def __getitem__(self, key):
        """
        """
        return self.data[key]