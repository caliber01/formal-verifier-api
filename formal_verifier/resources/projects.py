from flask_restful import Resource
from flask import request, abort
from flask_jwt_extended import get_jwt_identity, jwt_required

from formal_verifier import api, app
from formal_verifier.models import Project, User


class ProjectsList(Resource):

    @jwt_required
    def get(self):
        app.logger.info("QOOOOO")
        owner = User.objects(username=get_jwt_identity()).first()
        return Project.objects(owner=owner)

    @jwt_required
    def post(self):
        json = request.get_json()
        fields = {key: json[key] for key in json if key in Project._fields.keys()}
        project = Project(**fields)
        owner = User.objects(username=get_jwt_identity()).first()
        app.logger.info(owner)
        project.owner = owner
        project.models = []
        project.save()
        return project

api.add_resource(ProjectsList, '/projects')
