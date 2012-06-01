# -*- coding: utf-8 -*-
"""
mysolr.response
~~~~~~~~~~~~~

This module implements a class that encapsulate Http responses obtained from Solr.
mysolr.SolrResponse is a generic Solr Response, from any of the GET/POST methods
supported by mysolr. For example, performing a ping against a Solr instance will
return an object of class mysolr.SolrResponse.
Performing a search will also return a mysolr.SolrResponse object, but in this
case, the response will contain additional fields only relevant when working 
with search results.

Because mysolr uses requests library for all the Http machinery, a mysolr.SolrResponse
can be created from a more generic requests.Response.
"""

from .compat import parse_response
import requests
import json
import re
try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

class SolrResponse():
    """Parse solr response and make it accesible."""
    def __init__(self, http_response=None):
        """ Initializes a SolrResponse object.

        If a requests.Response is provided as an argument, some  of its attributes
        (headers, content, url and status_code) will be incorporated to the current 
        SolrResponse object.

        :param http_response: `requests.Response` object

        """
        if http_response is not None:
            self.headers = http_response.headers
            self.raw_response = http_response.content
            self.url = http_response.url
            self.status = http_response.status_code

        if self.raw_response:
            #try to parse raw content to know if its a Structured results response 
            #or an unstructured HTML page (usually resulting from an error)
            try:
                self.structured_body = parse_response(self.raw_response)
            except:
                self.structured_body = None

            if self.structured_body is not None: #Solr responded with a Structured Results Response
                #: Response status from solr responseHeader.
                self.solr_status = self.structured_body['responseHeader']['status']
                #: Query time.
                self.qtime = self.structured_body['responseHeader']['QTime']
                self.total_results = None
                self.start = None
                self.documents = None
                if 'response' in self.structured_body:
                    #: Number of results.
                    self.total_results = self.structured_body['response']['numFound']
                    #: Offset.
                    self.start = self.structured_body['response']['start']
                    #: Documents list.
                    self.documents = self.structured_body['response']['docs']
                #: Facets parsed as a OrderedDict (Order matters).
                self.facets = None
                if 'facet_counts' in self.structured_body:
                    self.facets = parse_facets(self.structured_body['facet_counts'])
                #: Shorcut to stats resuts
                self.stats = None
                if 'stats' in self.structured_body:
                    self.stats = self.structured_body['stats']['stats_fields']
                #: Spellcheck result parsed into a more readable object.
                self.spellcheck = None
                if 'spellcheck' in self.structured_body:
                    suggestions = self.structured_body['spellcheck']['suggestions']
                    self.spellcheck = parse_spellcheck(suggestions)
                #: Shorcut to highlighting result
                self.highlighting = None
                if 'highlighting' in self.structured_body:
                    self.highlighting = self.structured_body['highlighting']
                self.mlt = None
                if 'moreLikeThis' in self.structured_body:
                    self.mlt = self.structured_body['moreLikeThis']
                self.message = None
            else: #Solr responded with a unstructured HTML Body Response
                #try to extract error message from html body if any:
                self.message = self.extract_errmessage()

    def __repr__(self):
        return '<SolrResponse status=%d>' % self.status 

    def parse_facets(solr_facets):
        """ Parse facets."""
        result = {}
        for facet_type, facets in solr_facets.items():
            facet_type_dict = {}
            for name, facet in facets.items():
                if isinstance(facet, list):
                    parsed = [tuple(facet[i:i+2]) for i in range(0, len(facet), 2)]
                    facet_type_dict[name] = OrderedDict(parsed)
                elif isinstance(facet, dict):
                    facet_type_dict[name] = OrderedDict(facet)
                elif isinstance(facet, int):
                    facet_type_dict[name] = facet
            result[facet_type] = facet_type_dict
        return result


    def parse_spellcheck(solr_suggestions):
        """ Parse spellcheck result into a more readable format. """
        result = {}
        suggestions = {}

        for i in range(0, len(solr_suggestions), 2):
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

    def extract_errmessage(self):
        """Tries to extract an error message from a SolrResponse body content.
        
        Useful for error identification (e.g.: indexation errors)
        """
        message = None
        try:
            message = re.findall('<u>([^<]*)</u>', str(self.raw_response))[-1]
        except Exception as e:
            pass
        return message

