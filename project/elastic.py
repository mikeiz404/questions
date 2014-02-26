from elasticsearch import Elasticsearch

DEFAULT_URI = 'localhost:9200'
DEFAULT_SNIFF = False

def get_elastic_search(request):
    uri = request.registry.settings.get('elastic.uri', DEFAULT_URI)
    sniff = request.registry.settings.get('elastic.sniff_on_start', DEFAULT_SNIFF)
    return Elasticsearch(uri, sniff_on_start=sniff)

def get_es_search(request):
    es = request.elastic_search
    index = request.registry.settings['elastic.index']
    doc_type = request.registry.settings['elastic.doc_type']
    def es_search(body):
        es.search(index=index, doc_type=doc_type, body=body)
    return es_search

def get_es_index(request):
    es = request.elastic_search
    index = request.registry.settings['elastic.index']
    doc_type = request.registry.settings['elastic.doc_type']
    def es_index(body):
        es.index(index=index, doc_type=doc_type, body=body)
    return es_index