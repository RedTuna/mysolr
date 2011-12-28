.. mysolr documentation master file, created by
   sphinx-quickstart on Wed Aug 31 09:39:29 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to mysolr's documentation!
==================================

mysolr was born to be a fast and easy-to-use client for Apache Solr's API and because 
existing Python clients didn't fulfill these conditions.


Basic Usage
-----------
::

    from mysolr import Solr

    # Default connection to localhost:8080
    solr = Solr()

    # All solr params are supported!
    query = {'q' : '*:*', 'facet' : 'true', 'facet.field' : 'foo'}
    response = solr.search(**query)

    # do stuff with documents
    for document in response.documents:
        # modify field 'foo'
        document['foo'] = 'bar'

    # update index with modified documents
    solr.update(response.documents, commit=True)


Contents
--------

.. toctree::
   :maxdepth: 2

   user/installation
   user/userguide
   user/recipes
   api/classes
   user/benchmark

References
----------

We would like to thank the following developers their work and inspiration:

* The Apache Solr_ 's committers_
* Kenneth Reitz, Requests_ creator

Related projects
----------------

Other Python projects Apache Solr related:

* solrpy_
* pysolr_
* djangosolr_


.. _solrpy: http://code.google.com/p/solrpy/
.. _pysolr: https://github.com/toastdriven/pysolr/
.. _djangosolr: https://github.com/sophilabs/django-solr
.. _Requests: http://docs.python-requests.org/
.. _Solr: http://lucene.apache.org/solr/
.. _committers: http://lucene.apache.org/java/docs/whoweare.html
