from flask_restful import Resource
from flask import request, abort
from flask_jwt_extended import get_jwt_identity, jwt_required

from formal_verifier import api, app
from formal_verifier.models import Project, User
from formal_verifier.mappers import map_project_to_view_model


class ProjectsList(Resource):
    @jwt_required
    def get(self):
        owner = User.objects(username=get_jwt_identity()).first()
        return [map_project_to_view_model(project) for project in Project.objects(owner=owner)]

    @jwt_required
    def post(self):
        json = request.get_json()
        fields = {key: value for (key, value) in json.items() if key in Project._fields}
        project = Project(**fields)
        owner = User.objects(username=get_jwt_identity()).first()
        app.logger.info(owner)
        project.owner = owner
        project.models = []
        project.save()
        return map_project_to_view_model(project)


api.add_resource(ProjectsList, '/projects')
