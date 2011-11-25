.. _userguide:


User Guide
==========

Connecting to Solr
------------------

Use mysolr.Solr object for connecting to a Solr instance.

::

    from mysolr import Solr

    # Default connection. Connecting to http://localhost:8080/solr/
    solr = Solr()

    # Custom connection
    solr = Solr('http://foo.bar:9090/solr/')


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
using pagination would be like this ::

    from mysolr import Solr

    solr = Solr()

    # Get 10 documents
    response = solr.search(q='*:*', rows=10, start=0)


Facets
------

This is a query an example using facets with mysolr.

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

Facets are parsed and can be accessed by getting :attr:`~mysolr.SolrResponse.facets`
attribute of the SolrResponse object. Facets look like this::

    {
        'facet_dates': {},
        'facet_fields': {'foo': {'value1': 2, 'value2': 2}},
        'facet_queries': {},
        'facet_ranges': {}
    }


Spellchecker
------------

This is an example of a query that uses spellcheck component.

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


Spellchecker result is parsed and can be accessed by getting 
:attr:`~mysolr.SolrResponse.spellcheck` attribute of the SolrResponse object.::

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

:attr:`~mysolr.SolrResponse.stats` attribute is just a shorcut to stats result. So
it is not parsed and has the format that Solr sends.


Highlighting
------------

Like stats :attr:`~mysolr.SolrResponse.highlighting` is just a shorcut.


Concurrent searchs
------------------

As mysolr is using requests, it is posible to make concurrent queries thank to
requests.async ::

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

.. admonition:: Using concurrent searchs

    It's needed Gevent module for using requests.async so if you need concurrent
    searchs you have to install Gevent


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