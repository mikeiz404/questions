from mongoengine import Document
from mongoengine import StringField

class Question(Document):
    content = StringField(required=True)