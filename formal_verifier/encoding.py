from flask import make_response, jsonify
import bson.json_util
from formal_verifier import api, app
from mongoengine.fields import QuerySet
from mongoengine import Document


def convert_to_json(data):
    print(type, data)
    if isinstance(data, QuerySet) or isinstance(data, Document):
        return data.to_json()
    elif isinstance(data, dict):
        return bson.json_util.dumps(data)
    else:
        return jsonify(data)


def custom_json_output(data, code, headers=None):
    app.logger.info("Custom converter")
    dumped = convert_to_json(data)
    resp = make_response(dumped, code)
    resp.headers.extend(headers or {})
    return resp


api.representations.update({
    'application/json': custom_json_output
})
