mysolr
======

Fast python solr binding

Instalation
-----------

From source code: ::

  python setup.py install


Usage
-----

Search
......

    >>> from mysolr import Solr
    >>> solr = Solr()
    >>> response = solr.search(q='*:*')
    >>> response.status
    0
    >>> response.qtime
    1
    >>> response.start
    0
    >>> response.total_results
    1394500
    >>> response.documents
    [{...},...]