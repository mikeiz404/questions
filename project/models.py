from project.document import ElasticSyncedDocument

class Question(ElasticSyncedDocument):
    mongo_config = {'db': 'app22569342', 'collection': 'questions'}
    elastic_config = {'index': 'project', 'type': 'questions'}