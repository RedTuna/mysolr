.. image:: https://secure.travis-ci.org/RedTuna/mysolr.png?branch=master
   :target: https://secure.travis-ci.org/RedTuna/mysolr
   
.. image:: https://coveralls.io/repos/RedTuna/mysolr/badge.png?branch=dev
   :target: https://coveralls.io/r/RedTuna/mysolr?branch=dev
   
.. image:: https://pypip.in/d/mysolr/badge.png
   :target: https://pypi.python.org/pypi/mysolr/

.. image:: https://pypip.in/license/mysolr/badge.png
   :target: https://pypi.python.org/pypi/mysolr/


mysolr
======

Fast python solr binding. Check full documentation here_


Features
--------

* Full query syntax support
* Facets support
* Highlighting support
* Spellchecker support
* More like this support
* Stats support
* Concurrent searchs
* Python 3 compatible


Installation
------------

From source code: ::

  python setup.py install

From pypi: ::

  pip install mysolr


Usage
-----
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


.. _here: http://mysolr.redtuna.org
