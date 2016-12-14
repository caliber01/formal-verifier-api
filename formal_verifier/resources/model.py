from flask_restful import Resource
from flask import request, abort
from flask_jwt_extended import get_jwt_identity, jwt_required
from fmse_tool.cli.input_parser import parse_ctl_lts

from formal_verifier import api
from formal_verifier.mappers import map_lts_to_mongo, map_lts_to_view_model
from formal_verifier.models import Project


class ModelResource(Resource):
    @jwt_required
    def put(self, project_id, model_id):
        json = request.get_json()
        model_source = json['model_source']
        new_model = parse_ctl_lts(model_source)
        project = Project.objects(id=project_id).first()
        if project is None or not project.owner.username == get_jwt_identity():
            return abort(404)

        original_model = project.models[int(model_id)]
        updated_model = map_lts_to_mongo(new_model)
        updated_model.name = original_model.name
        project.models[int(model_id)] = updated_model
        project.save()
        return map_lts_to_view_model(updated_model)


api.add_resource(ModelResource, '/projects/<project_id>/models/<model_id>')
