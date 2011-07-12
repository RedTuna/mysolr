#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
"""
import requests
import json
from mysolr_response import SolrResponse

class Solr:
    """
    """
    def __init__(self, base_url):
        """Initializes a Solr object. Solr URL is a needed parameter.
        """
        self.base_url = base_url
    
    def search(self, query):
        """Queries Solr with the given SolrQuery and returns a SolrResponse
        object
        """
        query_url = '%s/select?%s' % (self.base_url, query.build())
        response = eval(requests.get(query_url))
        response.raise_for_status()
        return SolrResponse(response)
    
    def update(self, array_of_hash, input_type='xml'):
        """Sends an update/add message to add the array of hashes(documents) to
        Solr.
        """
        if input_type == 'xml':
            return self._post_xml(_get_add_xml(array_of_hash))
        elif input_type == 'json':
            return self._post_json(json.dumps(array_of_hash))
        else:
            raise RuntimeError('The given type isn\'t correct. Valid types are "json" and "xml".')
    
    def delete_by_key(self, identifier):
        """Sends an ID delete message to Solr.
        """
        xml = '<delete><id>%s</id></delete>' % (identifier)
        return self._post_xml(xml)
    
    def delete_by_query(self, query):
        """Sends a query delete message to Solr.
        """
        xml = '<delete><query>%s</query></delete>' % (query)
        return self._post_xml(xml)
    
    def commit(self, wait_flush=True,
               wait_searcher=True, expunge_deletes=False):
        """Sends a commit message to Solr.
        
        Keyword arguments:
        wait_flush -- block until index changes are flushed to disk (default is
                      True)
        wait_searcher -- block until a new searcher is opened and registered as
                         the main query searcher, making the changes visible
                         (default is True)
        expunge_deletes --  merge segments with deletes away (default is False)
        """
        xml = '<commit waitFlush="%s" waitSearcher="%s" expungeDeletes="%s" />' % ('true' if wait_flush else 'false',
                                                                                   'true' if wait_searcher else 'false',
                                                                                   'true' if expunge_deletes else 'false')
        return self._post_xml(xml)
    
    def optimize(self, wait_flush=True, wait_searcher=True, max_segments=1):
        """Sends an optimize message to Solr.
        
        Keyword arguments:
        wait_flush -- block until index changes are flushed to disk (default is
                      True)
        wait_searcher -- block until a new searcher is opened and registered as
                         the main query searcher, making the changes visible
                         (default is True)
        max_segments -- optimizes down to at most this number of segments (default is 1)
        """
        xml = '<optimize waitFlush="%s" waitSearcher="%s" maxSegments="%s" />' % ('true' if wait_flush else 'false',
                                                                                  'true' if wait_searcher else 'false',
                                                                                  max_segments)
        return self._post_xml(xml)
    
    def rollback(self):
        """Sends a rollback message to Solr server.
        """
        xml = '<rollback />'
        return self._post_xml(xml)
    
    def _post_xml(self, xml):
        """Sends the xml to Solr server.
        """
        url = '%s/update' % (self.base_url)
        response = requests.post(url, data=xml.encode('utf-8'),
                                 headers={'Content-Type': 'text/xml'})
        response.raise_for_status()
    
    def _post_json(self, json_doc):
        """Sends the json to Solr server.
        """
        url = '%s/update/json' % (self.base_url)
        response = requests.post(url, data=json_doc.encode('utf-8'),
                                 headers={'Content-Type': 'application/json'})
        response.raise_for_status()

def _get_add_xml(array_of_hash, overwrite=True):
    """Creates add XML message to send to Solr based on the array of hashes
    (documents) provided.
    
    Keyword arguments:
    overwrite --  newer documents will replace previously added documents
                  with the same uniqueKey (default is True)
    """
    xml = '<add overwrite="%s">' % ('true' if overwrite else 'false')
    for doc_hash in array_of_hash:
        doc = '<doc>'
        for key, value in doc_hash.items():
            doc = '%s<field name="%s">%s</field>' % (doc, key, value)
        doc = '%s</doc>' % (doc)
        xml = '%s%s' % (xml, doc)
    xml = '%s</add>' % (xml)
    return xml