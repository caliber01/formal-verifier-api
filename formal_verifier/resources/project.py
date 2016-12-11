from flask_restful import Resource
from flask import request, abort
from flask_jwt_extended import get_jwt_identity, jwt_required

from formal_verifier import api
from formal_verifier.models import Project


class Project(Resource):

    @jwt_required
    def get(self, project_id):
        project = Project.objects(id=project_id).first()
        if project is None or not project.owner.username == get_jwt_identity():
            return abort(404)
        return project

    @jwt_required
    def delete(self, project_id):
        project = Project.objects(id=project_id).first()

        if project is None or not project.owner.username == get_jwt_identity():
            return abort(404)
        project.delete()

    @jwt_required
    def put(self, project_id):
        project = Project.objects(id=project_id)
        if project is None or not project.owner.username == get_jwt_identity():
            return abort(404)
        update = request.get_json()
        for key in update:
            setattr(project, key, update[key])
        project.save()
        return project


api.add_resource(Project, '/projects/<project_id>')
