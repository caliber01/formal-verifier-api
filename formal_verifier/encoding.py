from flask import make_response, jsonify
import bson.json_util
from formal_verifier import api, app


def convert_to_json(data):
    if hasattr(data, 'to_json'):
        return data.to_json()
    else:
        return bson.json_util.dumps(data)


def custom_json_output(data, code, headers=None):
    app.logger.info("Custom converter")
    dumped = convert_to_json(data)
    resp = make_response(dumped, code)
    resp.headers.extend(headers or {})
    return resp


api.representations.update({
    'application/json': custom_json_output
})
