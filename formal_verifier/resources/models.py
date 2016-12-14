from flask import request, abort
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource

from formal_verifier import api
from formal_verifier.models import Project
from formal_verifier.mappers import map_lts_to_view_model


class ModelsList(Resource):

    @jwt_required
    def post(self, project_id):
        json = request.get_json()
        project = Project.objects(id=project_id).first()
        if project is None or not project.owner.username == get_jwt_identity():
            return abort(404)

        model = project.models.create(name=json['name'])
        project.save()
        return map_lts_to_view_model(model)


api.add_resource(ModelsList, '/projects/<project_id>/models')
