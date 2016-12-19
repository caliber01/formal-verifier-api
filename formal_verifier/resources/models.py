from bson.json_util import dumps
from flask import request, abort
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource

from formal_verifier import api, app
from formal_verifier.models import Project
from formal_verifier.mappers import map_lts_to_view_model, map_lts_from_mongo, map_lts_to_mongo


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


@app.route('/projects/<project_id>/models/compose', methods=['POST'])
@jwt_required
def compose_model(project_id):
    json = request.get_json()
    project = Project.objects(id=project_id).first()
    if project is None or not project.owner.username == get_jwt_identity():
        return abort(404)

    first_model = project.models.filter(_id=json['first_model_id']).first()
    second_model = project.models.filter(_id=json['second_model_id']).first()
    first_lts = map_lts_from_mongo(first_model)
    second_lts = map_lts_from_mongo(second_model)
    composed_lts = first_lts.compose(second_lts)
    composed = map_lts_to_mongo(composed_lts)
    composed.name = json['name']
    composed.source = generate_source_for_lts(composed_lts)
    project.update(push__models=composed)
    return dumps(map_lts_to_view_model(composed))


def format_transitions(transitions):
    return ", ".join(
        token + ' -> ' + "_".join(to_state)
        for (_, token, to_state) in transitions
    )


def generate_source_for_lts(lts):
    return ";\n".join(
        "_".join(state) + " {" + ", ".join(lts.labellings[state]) + "} " +
        "(" + format_transitions(lts.get_transitions_from_state(state)) + ")"
        for state in lts.get_states()
    ) + ";\n"


