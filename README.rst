mysolr
======

Fast python solr binding

Instalation
-----------

From source code: ::

  python setup.py install
  

Solr Configuration
..................

To update Solr Index using JSON, a few lines must be added at Solr's **config.xml**: ::

    <requestHandler name="/update/json" class="solr.JsonUpdateRequestHandler" startup="lazy" />


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