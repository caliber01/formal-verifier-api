from flask_restful import Resource
from flask import request, abort
from flask_jwt_extended import get_jwt_identity, jwt_required
from fmse_tool.cli.input_parser import parse_ctl_lts

from formal_verifier import api
from formal_verifier.mappers import map_lts_to_mongo, map_lts_to_view_model
from formal_verifier.models import Project


class ModelResource(Resource):
    @jwt_required
    def put(self, project_id, model_name):
        json = request.get_json()
        model_source = json['source']
        new_model = parse_ctl_lts(model_source)
        project = Project.objects(id=project_id).first()
        if project is None or not project.owner.username == get_jwt_identity():
            return abort(404)

        original_model = project.models.filter(name=model_name).first()
        updated_model = map_lts_to_mongo(new_model)
        updated_model.name = original_model.name
        updated_model.save()
        return map_lts_to_view_model(updated_model)

    @jwt_required
    def patch(self, project_id, model_name):
        json = request.get_json()
        formulas = json['formulas']
        project = Project.objects(id=project_id).first()
        if project is None or not project.owner.username == get_jwt_identity():
            return abort(404)

        model = project.models.filter(name=model_name).first()
        model.formulas = formulas
        model.save()
        return map_lts_to_view_model(model)


api.add_resource(ModelResource, '/projects/<project_id>/models/<model_name>')
