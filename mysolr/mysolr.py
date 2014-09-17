# -*- coding: utf-8 -*-
"""
mysolr.mysolr
~~~~~~~~~~~~~

This module impliments the mysolr Solr class, providing an easy access to
operate with a Solr server.

>>> from mysolr import Solr
>>> solr = Solr('http://myserver:8080/solr')
>>> query = {'q':'*:*', 'rows': 0, 'start': 0, 'facet': 'true', 
             'facet.field': 'province'}
>>> query_response = solr.search(**query)

"""
from .response import SolrResponse
from .compat import urljoin, compat_args, get_basestring
from xml.sax.saxutils import escape

import json
import requests

class Solr(object):
    """Acts as an easy-to-use interface to Solr."""

    def __init__(self, base_url='http://localhost:8080/solr/',
                 make_request=requests, use_get=False, version=None,
                 timeout=None):
        """ Initializes a Solr object. Solr URL is a needed parameter.

        :param base_url: Url to solr index
        :param make_request: 
        :param use_get: Use get instead of post when searching. Useful if you
                        cache GET requests
        :param version: first number of the solr version. i.e. 4 if solr 
                        version is 4.0.0 If you set to none this parameter
                        a request to admin/system will be done at init time
                        in order to guess the version.
        :param timeout: request timeout for all requests made to solr
        """
        self.base_url = base_url if base_url.endswith('/') else '%s/' % base_url
        self.make_request = make_request
        self.use_get = use_get
        self.version = version
        if not version:
            self.version = self.get_version()
        assert(self.version in (1, 3, 4))
        self.timeout = timeout

    def search(self, resource='select', **kwargs):
        """Queries Solr with the given kwargs and returns a SolrResponse
        object.

        :param resource: Request dispatcher. 'select' by default.
        :param **kwargs: Dictionary containing any of the available Solr query
                         parameters described in
                         http://wiki.apache.org/solr/CommonQueryParameters.
                         'q' is a mandatory parameter.

        """
        query = build_request(kwargs)
        url = urljoin(self.base_url, resource)
        if self.use_get:
            http_response = self.make_request.get(url, params=query,
                                                  timeout=self.timeout)
        else:
            http_response = self.make_request.post(url, data=query,
                                                   timeout=self.timeout)

        solr_response = SolrResponse(http_response)
        return solr_response

    def search_cursor(self, resource='select', **kwargs):
        """ """
        query = build_request(kwargs)
        cursor = Cursor(urljoin(self.base_url, resource), query,
                        self.make_request, self.use_get, timeout=self.timeout)

        return cursor
    
    def async_search(self, queries, size=10, resource='select'):
        """ Asynchronous search using async module from requests. 

        :param queries:  List of queries. Each query is a dictionary containing
                         any of the available Solr query parameters described in
                         http://wiki.apache.org/solr/CommonQueryParameters.
                         'q' is a mandatory parameter.
        :param size:     Size of threadpool
        :param resource: Request dispatcher. 'select' by default.
        """
        try:
            import grequests
        except:
            raise RuntimeError('grequests is required for Solr.async_search.')

        url = urljoin(self.base_url, resource)
        queries = map(build_request, queries)
        rs = (grequests.post(url, data=query) for query in queries)
        responses = grequests.map(rs, size=size)
        return [SolrResponse(http_response) for http_response in responses]


    def update(self, documents, input_type='json', commit=True):
        """Sends an update/add message to add the array of hashes(documents) to
        Solr.

        :param documents: A list of solr-compatible documents to index. You
                          should use unicode strings for text/string fields.
        :param input_type: The format which documents are sent. Remember that
                           json is not supported until version 3.
        :param commit: If True, sends a commit message after the operation is
                       executed.

        """
        assert input_type in ['xml', 'json']

        if input_type == 'xml':
            http_response = self._post_xml(_get_add_xml(documents))
        else:
            http_response = self._post_json(json.dumps(documents))
        if commit:
            self.commit()
        
        return SolrResponse(http_response)

    def delete_by_key(self, identifier, commit=True):
        """Sends an ID delete message to Solr.

        :param commit: If True, sends a commit message after the operation is
                       executed.

        """
        xml = '<delete><id>%s</id></delete>' % (identifier)
        http_response = self._post_xml(xml)
        if commit:
            self.commit()
        return SolrResponse(http_response)

    def delete_by_query(self, query, commit=True):
        """Sends a query delete message to Solr.

        :param commit: If True, sends a commit message after the operation is
                       executed.

        """
        xml = '<delete><query>%s</query></delete>' % (query)
        http_response = self._post_xml(xml)
        if commit:
            self.commit()
        return SolrResponse(http_response)

    def commit(self, wait_flush=True,
               wait_searcher=True, expunge_deletes=False):
        """Sends a commit message to Solr.

        :param wait_flush: Block until index changes are flushed to disk
                           (default is True).
        :param wait_searcher: Block until a new searcher is opened and
                              registered as the main query searcher, making the
                              changes visible (default is True).
        :param expunge_deletes: Merge segments with deletes away (default is 
                                False)

        """
        xml = '<commit '
        if self.version < 4:
            xml += 'waitFlush="%s" ' % str(wait_flush).lower()
        xml += 'waitSearcher="%s" ' % str(wait_searcher).lower()
        xml += 'expungeDeletes="%s" ' % str(expunge_deletes).lower()
        xml += '/>'

        http_response = self._post_xml(xml)
        return SolrResponse(http_response)

    def optimize(self, wait_flush=True, wait_searcher=True, max_segments=1):
        """Sends an optimize message to Solr.

        :param wait_flush: Block until index changes are flushed to disk
                           (default is True)
        :param wait_searcher: Block until a new searcher is opened and
                              registered as the main query searcher, making the
                              changes visible (default is True)
        :param max_segments: Optimizes down to at most this number of segments
                             (default is 1)

        """
        xml = '<optimize '
        if self.version < 4:
            xml += 'waitFlush="%s" ' % str(wait_flush).lower()
        xml += 'waitSearcher="%s" ' % str(wait_searcher).lower()
        xml += 'maxSegments="%s" ' % max_segments
        xml += '/>'

        http_response = self._post_xml(xml)
        return SolrResponse(http_response)

    def rollback(self):
        """Sends a rollback message to Solr server."""
        xml = '<rollback />'
        http_response = self._post_xml(xml)
        return SolrResponse(http_response)

    def ping(self):
        """ Ping call to solr server. """
        url = urljoin(self.base_url, 'admin/ping')
        http_response = self.make_request.get(url, params={'wt': 'json'},
                                              timeout=self.timeout)
        return SolrResponse(http_response)

    def is_up(self):
        """Check if a Solr server is up using ping call"""
        try:
            solr_response = self.ping()
        except:
            return False
        return solr_response.status == 200 and solr_response.solr_status == 0

    def schema(self):
        return self._get_file('schema.xml')

    def solrconfig(self):
        return self._get_file('solrconfig.xml')

    def get_system_info(self):
        """ Gets solr system status. """
        url = urljoin(self.base_url, 'admin/system')
        params = {'wt': 'json'}
        http_response = self.make_request.get(url, params=params,
                                              timeout=self.timeout)
        return SolrResponse(http_response)

    def get_version(self):
        system_info = self.get_system_info()
        version = system_info.raw_content['lucene']['solr-spec-version']
        return int(version[0])

    def more_like_this(self, resource='mlt', text=None, **kwargs):
        """Implements convenient access to Solr MoreLikeThis functionality  

        Please, visit http://wiki.apache.org/solr/MoreLikeThis to learn more
        about MLT configuration and common parameters.

        There are two ways of using MLT in Solr:

        Using a previously configured RequestHandler
            You normally specify a query and the first matching document for 
            that query is used to retrieve similar documents.
            You can however specify a text instead of a query, and similar
            documents to the text will be returned.
            You must configure a MLT RequestHandler in your solrconfig.xml in
            order to get advantage of this functionality.
            Note that this method has a default resource name with value "mlt",
            but if your RequestHandler has a different name you must specify it
            when calling the more_like_this method.

        Using the MLT Search Component:
            The resulting documents in this case will be those that match the
            regular query, but the SolrResponse will have a "mlt" section where
            similar documents for each result document will be given.

        :param resource: Request dispatcher. 'ml' by default.
        :param text: Text to use for similar documents retrieval. None by
                     default.
        :param **kwargs: Dictionary containing any of the available Solr query
                         parameters described in
                         http://wiki.apache.org/solr/CommonQueryParameters
                         or MoreLikeThis Common parameters described in
                         http://wiki.apache.org/solr/MoreLikeThis.
                         'q' is a mandatory parameter in all cases except
                         when using a MLT RequestHandler with a Text parameter.
    
        """
        if text is not None: #RequestHandler with Content-Streamed Text
            #we dont call build_query because 'q' is NOT mandatory in this case
            kwargs['wt'] = 'json'
            headers = {'Content-type': 'text/json'}
            url = urljoin(self.base_url, resource)
            http_response = self.make_request.post(url, params=kwargs,
                                                   data=text,
                                                   headers=headers,
                                                   timeout=self.timeout)
            solr_response = SolrResponse(http_response)
            return solr_response
        else:
            return self.search(resource=resource, **kwargs)

    def _post_xml(self, xml):
        """ Sends the xml to Solr server.

        :param xml: XML document to be posted.
        """
        url = urljoin(self.base_url, 'update')
        xml_data = xml.encode('utf-8')
        headers = {
            'Content-type': 'text/xml; charset=utf-8',
            'Content-Length': "%s" % len(xml_data)
        }
        http_response = self.make_request.post(url, data=xml_data,
                                               headers=headers,
                                               timeout=self.timeout)
        return http_response

    def _post_json(self, json_doc):
        """ Sends the json to Solr server.

        :param json_doc: JSON document to be posted.
        """
        url = urljoin(self.base_url, 'update/json')
        json_data = json_doc.encode('utf-8')
        headers = {
            'Content-type': 'application/json; charset=utf-8',
            'Content-Length': "%s" % len(json_data)
        }
        http_response = self.make_request.post(url, data=json_data,
                                               headers=headers)
        return http_response

    def _get_file(self, filename):
        """Retrieves config files of the current index."""
        url = urljoin(self.base_url, 'admin/file')
        params = {
            'contentType': 'text/xml;charset=utf-8',
            'file' : filename
        }
        http_response = self.make_request.get(url, params=params, timeout=self.timeout)
        return http_response.content


class Cursor(object):
    """ Implements the concept of cursor in relational databases """
    def __init__(self, url, query, make_request=requests, use_get=False, timeout=None):
        """ Cursor initialization """
        self.url = url
        self.query = query
        self.make_request = make_request
        self.use_get = use_get
        self.timeout = timeout

    def fetch(self, rows=None):
        """ Generator method that grabs all the documents in bulk sets of 
        'rows' documents

        :param rows: number of rows for each request
        """
        if rows:
            self.query['rows'] = rows

        if 'rows' not in self.query:
            self.query['rows'] = 10

        self.query['start'] = 0

        end = False
        docs_retrieved = 0
        while not end:
            if self.use_get:
                http_response = self.make_request.get(self.url,
                                                      params=self.query,
                                                      timeout=self.timeout)
            else:
                http_response = self.make_request.post(self.url,
                                                       data=self.query,
                                                       timeout=self.timeout)
            solr_response = SolrResponse(http_response)
            yield solr_response
            total_results = solr_response.total_results
            docs_retrieved += len(solr_response.documents)
            end = docs_retrieved == total_results
            self.query['start'] += self.query['rows']


def _get_add_xml(array_of_hash, overwrite=True):
    """ Creates add XML message to send to Solr based on the array of hashes
    (documents) provided.

    :param overwrite: Newer documents will replace previously added documents
                      with the same uniqueKey (default is True)

    """
    xml = '<add overwrite="%s">' % ('true' if overwrite else 'false')
    for doc_hash in array_of_hash:
        doc = '<doc>'
        for key, value in doc_hash.items():
            if isinstance(value, list):
                for v in value:
                    if isinstance(v, get_basestring()):
                        v = escape(v)
                    doc += '<field name="%s">%s</field>' % (key, v)
            else:
                if isinstance(value, get_basestring()):
                    value = escape(value)
                doc += '<field name="%s">%s</field>' % (key, value)
        doc += '</doc>'
        xml += doc
    xml += '</add>'
    return xml


def  build_request(query):
    """ Check solr query and put convenient format """
    assert 'q' in query
    compat_args(query)
    query['wt'] = 'json'
    return query
