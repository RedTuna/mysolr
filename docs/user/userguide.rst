.. _userguide:


User Guide
==========

Connecting to Solr
------------------

Use mysolr.Solr object to connect to a Solr instance.

::

    from mysolr import Solr

    # Default connection. Connecting to http://localhost:8080/solr/
    solr = Solr()

    # Custom connection
    solr = Solr('http://foo.bar:9090/solr/')

If the server is secured with HTTP basic authentication you can connect by 
using auth parameter.

::

    from mysolr import Solr

    solr = Solr(auth=('admin', 'admin'))


Further information about auth parameter in requests docs_


Queriying to Solr
-----------------

Making a query to Solr is very easy, just call search method with your query.

::

    from mysolr import Solr

    solr = Solr()
    # Search for all documents
    response = solr.search(q='*:*')
    # Get documents
    documents = response.documents

Besides, all available Solr query params are supported. So making a query
using pagination would be as simple as ::

    from mysolr import Solr

    solr = Solr()

    # Get 10 documents
    response = solr.search(q='*:*', rows=10, start=0)

Some parameters contain a period. In those cases you have to use a dictionary to
build the query::

    from mysolr import Solr

    solr = Solr()

    query = {'q' : '*:*', 'facet' : 'true', 'facet.field' : 'foo'}
    response = solr.search(**query)


Sometimes specifying a HTTP parameter multiple times is needed. For instance
when faceting by several fields. Use a list in that case.::

    from mysolr import Solr

    solr = Solr()

    query = {'q' : '*:*', 'facet' : 'true', 'facet.field' : ['foo', 'bar']}
    response = solr.search(**query)


Cursors
-------

The typical concept of cursor in relational databases is also implemented in 
mysolr.

::

    from mysolr import Solr

    solr = Solr()

    cursor = solr.search_cursor(q='*:*')

    # Get all the documents
    for response in cursor.fetch(100):
        # Do stuff with the current 100 documents
        pass


Facets
------

This is a query example using facets with mysolr.

::

    from mysolr import Solr

    solr = Solr()
    # Search for all documents facets by field foo
    query = {'q' : '*:*', 'facet' : 'true', 'facet.field' : 'foo'}
    response = solr.search(**query)
    # Get documents
    documents = response.documents
    # Get facets
    facets = response.facets

Facets are parsed and can be accessed by retrieving :attr:`~mysolr.SolrResponse.facets`
attribute from the SolrResponse object. Facets look like this::

    {
        'facet_dates': {},
        'facet_fields': {'foo': OrderedDict[('value1', 2), ('value2', 2)]},
        'facet_queries': {},
        'facet_ranges': {}
    }

Ordered dicts are used to store the facets because order matters.

In any case, if you don't like how facets are parsed you can use 
:attr:`~mysolr.SolrResponse.raw_content` attribute which contains the raw
response from solr.


Spellchecker
------------

This is an example of a query that uses the spellcheck component.

::

    from mysolr import Solr

    solr = Solr()

    # Spell check query
    query = {
        'q' : 'helo wold',
        'spellcheck' : 'true',
        'spellcheck.collate': 'true',
        'spellcheck.build':'true'
    }

    response = solr.search(**query)


Spellchecker results are parsed and can be accessed by getting the 
:attr:`~mysolr.SolrResponse.spellcheck` attribute from the SolrResponse object.::

    {'collation': 'Hello world',
    'correctlySpelled': False,
    'suggestions': {
                    'helo': {'endOffset': 4,
                                 'numFound': 1,
                                 'origFreq': 0,
                                 'startOffset': 0,
                                 'suggestion': [{'freq': 14,
                                                 'word': 'hello'}]},
                    'wold': {'endOffset': 9,
                             'numFound': 1,
                             'origFreq': 0,
                             'startOffset': 5,
                             'suggestion': [{'freq': 14, 'word': 'world'}]}}}

Stats
-----

:attr:`~mysolr.SolrResponse.stats` attribute is just a shortcut to stats result.
It is not parsed and has the format sent by Solr.


Highlighting
------------

Like stats, :attr:`~mysolr.SolrResponse.highlighting` is just a shortcut.


Concurrent searchs
------------------

As mysolr is using requests, it is posible to make concurrent queries thanks to
grequest ::

    from mysolr import Solr
    solr = Solr()
    # queries
    queries = [
        {
            'q' : '*:*'
        },
        {
            'q' : 'foo:bar'
        }
    ]

    # using 10 threads
    responses = solr.async_search(queries, size=10)

See :ref:`installation <installation>` section for further information about how
to install this feature.


Indexing documents
------------------
::

    from mysolr import Solr

    solr = Solr()

    # Create documents
    documents = [
        {'id' : 1,
         'field1' : 'foo'
        },
        {'id' : 2,
         'field2' : 'bar'
        } 
    ]
    # Index using json is faster!
    solr.update(documents, 'json', commit=False)

    # Manual commit
    solr.commit()

.. _docs: http://docs.python-requests.org/en/latest/user/quickstart/#basic-authentication