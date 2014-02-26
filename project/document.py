from elasticsearch import Elasticsearch
from pymongo import MongoClient
from bson import ObjectId

class MongoDocument(dict):
    """
    A bare bones implementation of a mongo document.
    TODO: implement better error handling
    TODO: add tests
    """
    _id = None
    _mongodb = None
    mongo_config = {}

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if key == '_id':
                self._id = str(value)
            else:
                self[key] = value

    def to_mongo(self):
        data = dict(self)
        if self._id is not None:
            data['_id'] = ObjectId(self._id)
        return data

    def save(self):
        db = self.mongo_config.get('db')
        collection = self.mongo_config.get('collection')
        object_id = self._mongodb[db][collection].save(self.to_mongo())
        # update id
        self._id = str(object_id)

    def delete(self):
        if self._id is not None:
            db = self.mongo_config.get('db')
            collection = self.mongo_config.get('collection')
            self._mongodb[db][collection].remove({"_id": ObjectId(self._id)})
            # update id
            self._id = None
        else:
            raise 'Object _id is None.'

    @classmethod
    def search(clazz, *args, **kwargs):
        db = clazz.mongo_config.get('db')
        collection = clazz.mongo_config.get('collection')
        results = clazz._mongodb[db][collection].find(*args, **kwargs)
        for result in results:
            object = clazz(**result)
            yield object


class ElasticSyncedDocument(MongoDocument):
    """
    A bare bones implementation of an elastic search synced mongo document.
    TODO: implement better error handling
    TODO: use a connection pool instead of class based connections
    TODO: add tests
    """
    _elastic = None
    elastic_config = {'index': None, 'type': None}

    def to_elastic(self):
        return dict(self)

    def save_elastic(self):
        assert(self._id is not None)
        index = self.elastic_config.get('index')
        type = self.elastic_config.get('type')
        self._elastic.index(index, type, id=self._id, body=self.to_elastic())

    def save(self):
        super(ElasticSyncedDocument, self).save()
        self.save_elastic()

    def delete_elastic(self):
        if self._id is not None:
            index = self.elastic_config.get('index')
            type = self.elastic_config.get('type')
            self._elastic.delete(index, type, self._id)
        else:
            raise 'Object _id is None.'


    def delete(self):
        self.delete_elastic()
        super(ElasticSyncedDocument, self).delete()

    @classmethod
    def search_elastic(clazz, body):
        index = clazz.elastic_config.get('index')
        type = clazz.elastic_config.get('type')
        results = clazz._elastic.search(index, type, body)
        # reconstitute
        for data in results['hits']['hits']:
            object = clazz(_id=data['_id'], **(data['_source']))
            yield object

    @classmethod
    def search_mongo(clazz, *args, **kwargs):
        return super(ElasticSyncedDocument, clazz).search(*args, **kwargs)


def includeme(config):
    settings = config.registry.settings
    # create connections
    mongodb = MongoClient(settings['mongo.uri'])
    elastic = Elasticsearch(settings['elastic.uri'])
    # inject in models
    MongoDocument._mongodb = mongodb
    ElasticSyncedDocument._elastic = elastic