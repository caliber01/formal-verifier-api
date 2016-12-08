from formal_verifier import app
from mongoengine import *
from bson.json_util import dumps

connect()


class User(Document):
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    username = StringField(required=True, unique=True)
    email = StringField(require=True, unique=True)
    is_authenticated = BooleanField()
    is_active = BooleanField(required=True)
    is_anonymous = BooleanField()
    session_token = StringField()
    password_hash = BinaryField()

    def get_id(self):
        return str(self.session_token)

    @staticmethod
    def get_field_names():
        return User._fields.keys()

    def to_json(self, *args, **kwargs):
        data = self.to_mongo()
        data.pop('password_hash', None)
        return dumps(data)


class Transition(EmbeddedDocument):
    from_state = ListField(StringField(required=True))
    to_state = ListField(StringField(required=True))
    token = StringField(required=True)


class Labelling(EmbeddedDocument):
    state = ListField(StringField(required=True))
    labels = ListField(StringField(required=True))


class LTS(Document):
    author = ReferenceField(User)
    transitions = ListField(EmbeddedDocumentField(Transition))
    labellings = ListField(EmbeddedDocumentField(Labelling))

