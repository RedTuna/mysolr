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

    # Get the number of documents of the source index
    n_documents = solr_source.search(q='*:*', rows=0).total_results

    for start in range(0, n_documents, PACKET_SIZE):
        resp = solr_source.search(q='*:*', rows=PACKET_SIZE, start=start)
        source_docs = resp.documents
        solr_target.update(source_docs)