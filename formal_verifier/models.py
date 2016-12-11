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
    password_hash = BinaryField()

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


class LTS(EmbeddedDocument):
    transitions = EmbeddedDocumentListField(Transition)
    labellings = EmbeddedDocumentListField(Labelling)


class Project(Document):
    owner = ReferenceField(User, required=True)
    name = StringField(required=True)
    description = StringField(required=True)
    models = EmbeddedDocumentListField(LTS)

