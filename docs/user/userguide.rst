.. _userguide:


User Guide
==========

Connecting to Solr
------------------
::

    from mysolr import Solr

    # Default connection. Connecting to http://localhost:8080/solr/
    solr = Solr()

    # Custom connection
    solr = Solr('http://foo.bar:9090/solr/')


Queriying to Solr
-----------------
::

    from mysolr import Solr

    solr = Solr()
    # Search for all documents
    response = solr.search(q='*:*')
    # Get documents
    documents = response.documents

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