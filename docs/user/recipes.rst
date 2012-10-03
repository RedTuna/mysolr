.. _recipes:

Recipes
=======

Solr backup
-----------
How to copy all documents from one solr server to another. ::

    from mysolr import Solr

    PACKET_SIZE = 5000

    solr_source = Solr('http://server1:8080/solr/')
    solr_target = Solr('http://server2:8080/solr/')

    cursor = solr_source.search_cursor(q='*:*')

    for resp in cursor.fetch(PACKET_SIZE):
        source_docs = resp.documents
        solr_target.update(source_docs)