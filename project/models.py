from elasticsearch import Elasticsearch
from pymongo import MongoClient
from bson import ObjectId

class SyncedDocument(dict):
    """
    A bare bones implementation of an elastic search synced mongo document.
    TODO: implement better error handling
    TODO: use a connection pool instead of class based connections
    TODO: add tests
    """
    _id = None
    elastic = Elasticsearch()
    mongodb = MongoClient()
    _mongo = {'db': None, 'collection': None}
    _elastic = {'index': None, 'type': None}

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

    def to_elastic(self):
        return dict(self)

    def save_elastic(self):
        assert(self._id is not None)
        index = self._elastic.get('index')
        type = self._elastic.get('type')
        self.elastic.index(index, type, id=self._id, body=self.to_elastic())

    def save_mongo(self):
        db = self._mongo.get('db')
        collection = self._mongo.get('collection')
        object_id = self.mongodb[db][collection].save(self.to_mongo())
        # update id
        self._id = str(object_id)

    def save(self):
        self.save_mongo()
        self.save_elastic()

    def delete_elastic(self):
        if self._id is not None:
            index = self._elastic.get('index')
            type = self._elastic.get('type')
            self.elastic.delete(index, type, self._id)
        else:
            raise 'Object _id is None.'

    def delete_mongo(self):
        if self._id is not None:
            db = self._mongo.get('db')
            collection = self._mongo.get('collection')
            self.mongodb[db][collection].remove({"_id": ObjectId(self._id)})
            # update id
            self._id = None
        else:
            raise 'Object _id is None.'

    def delete(self):
        self.delete_elastic()
        self.delete_mongo()

    @classmethod
    def search_elastic(clazz, body):
        index = clazz._elastic.get('index')
        type = clazz._elastic.get('type')
        results = clazz.elastic.search(index, type, body)
        # reconstitute
        for data in results['hits']['hits']:
            object = clazz(_id=data['_id'], **(data['_source']))
            yield object

    @classmethod
    def search_mongo(clazz, *args, **kwargs):
        db = clazz._mongo.get('db')
        collection = clazz._mongo.get('collection')
        results = clazz.mongodb[db][collection].find(*args, **kwargs)
        for result in results:
            object = clazz(**result)
            yield object

class Question(SyncedDocument):
    _mongo = {'db': 'project', 'collection': 'questions'}
    _elastic = {'index': 'project', 'type': 'questions'}