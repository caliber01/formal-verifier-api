from collections import defaultdict
from fmse_tool.model.CTLLTS import CTLLTS
from fmse_tool.model.Transition import Transition
from fmse_tool.cli.diagram_generator import generate_extended_diagram

from formal_verifier.models import LTS as MongoLTS, Transition as MongoTransition, Labelling as MongoLabelling


def map_lts_to_mongo(lts):
    initial_state = list(lts.initial_state)
    transitions = [
        MongoTransition(from_state=list(from_state), token=token, to_state=list(to_state))
        for (from_state, token, to_state) in lts.transitions
    ]
    labellings = [
        MongoLabelling(state=list(state), labels=list(labels))
        for (state, labels) in lts.labellings.items()
        ]
    return MongoLTS(initial_state=initial_state, transitions=transitions, labellings=labellings)


def map_transition_from_mongo(transition):
    return Transition(
        from_state=tuple(transition.from_state),
        token=transition.token,
        to_state=tuple(transition.to_state)
    )


def map_lts_from_mongo(lts):
    initial_state = tuple(lts.initial_state)
    transitions = [
        map_transition_from_mongo(transition)
        for transition in lts.transitions
    ]
    labellings = defaultdict(set, {
        tuple(labelling.state): labelling.labels
        for labelling in lts.labellings
    })
    return CTLLTS(transitions, initial_state, labellings)


def map_user_to_view_model(user):
    data = user.to_mongo()
    data.pop('password_hash', None)
    return data


def map_lts_to_view_model(model):
    lts = map_lts_from_mongo(model)
    name = model.name
    graph = generate_extended_diagram(lts, set())
    return {
        'name': name,
        'graph': graph
    }


def map_project_to_view_model(project):
    data = project.to_mongo()
    data['models'] = [
        map_lts_to_view_model(model)
        for model in project.models
        ]
    return data

