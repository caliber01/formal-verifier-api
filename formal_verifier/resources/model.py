from flask_restful import Resource
from flask import request, abort, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from fmse_tool.parsing.model.parser import parse_ctllts
from fmse_tool.parsing.parser import parse_formula
from fmse_tool.cli.diagram_generator import generate_extended_diagram

from formal_verifier import api, app
from formal_verifier.mappers import map_lts_to_mongo, map_lts_to_view_model, map_lts_from_mongo
from formal_verifier.models import Project


class ModelResource(Resource):
    @jwt_required
    def put(self, project_id, model_id):
        json = request.get_json()
        model_source = json['source']
        new_model = parse_ctllts(model_source)
        project = Project.objects(id=project_id).first()
        if project is None or not project.owner.username == get_jwt_identity():
            return abort(404)

        original_model = project.models.filter(_id=model_id).first()
        updated_model = map_lts_to_mongo(new_model)
        original_model.source = model_source
        original_model.initial_state = updated_model.initial_state
        original_model.transitions = updated_model.transitions
        original_model.labellings = updated_model.labellings
        original_model.save()
        return map_lts_to_view_model(original_model)

    @jwt_required
    def patch(self, project_id, model_id):
        json = request.get_json()
        formulas = json['formulas']
        project = Project.objects(id=project_id).first()
        if project is None or not project.owner.username == get_jwt_identity():
            return abort(404)

        # try parse all the formulas
        for formula in formulas:
            parse_formula(formula)

        model = project.models.filter(_id=model_id).first()
        model.formulas = formulas
        model.save()
        return map_lts_to_view_model(model)


api.add_resource(ModelResource, '/projects/<project_id>/models/<model_id>')


@app.route('/projects/<project_id>/models/<model_id>/check', methods=['POST'])
@jwt_required
def check_model(project_id, model_id):
    project = Project.objects(id=project_id).first()
    model = project.models.filter(_id=model_id).first()
    lts = map_lts_from_mongo(model)
    checked_graphs = {
        formula: {
            'graph': generate_extended_diagram(lts, valid_states),
            'valid': len(valid_states) > 0
        }
        for (formula, valid_states) in (
            (formula, parse_formula(formula).evaluate(lts, lts.get_states()))
            for formula in model.formulas
        )
    }
    return jsonify(checked_graphs)
