from project.document import ElasticSyncedDocument

class Question(ElasticSyncedDocument):
    mongo_config = {'db': 'project', 'collection': 'questions'}
    elastic_config = {'index': 'project', 'type': 'questions'}