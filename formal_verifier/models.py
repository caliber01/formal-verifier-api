from mongoengine import *

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


class Transition(EmbeddedDocument):
    from_state = ListField(StringField(required=True))
    to_state = ListField(StringField(required=True))
    token = StringField(required=True)


class Labelling(EmbeddedDocument):
    state = ListField(StringField(required=True))
    labels = ListField(StringField(required=True))


class LTS(EmbeddedDocument):
    name = StringField(unique=True, required=True)
    initial_state = ListField(StringField(required=True))
    transitions = EmbeddedDocumentListField(Transition)
    labellings = EmbeddedDocumentListField(Labelling)
    formulas = ListField(StringField(required=True))


class Project(Document):
    owner = ReferenceField(User, required=True)
    name = StringField(required=True)
    description = StringField(required=True)
    models = EmbeddedDocumentListField(LTS)

