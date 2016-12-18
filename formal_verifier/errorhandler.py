from flask import jsonify
from mongoengine import ValidationError, NotUniqueError
from fmse_tool.parsing.exception import ParsingError

from . import app


@app.errorhandler(401)
def handle_401(error):
    app.logger.error(error)
    return jsonify({'message': 'Unauthorized'}), 401, {'WWWAuthenticate': 'Basic realm="Login Required"'}


@app.errorhandler(ParsingError)
def handle_parsing_error(error):
    return jsonify({'message': str(error)}), 400


for errorType in [400, ValidationError, NotUniqueError]:
    @app.errorhandler(errorType)
    def handle_validation_error(error):
        app.logger.error(error)
        return jsonify({'Bad request'}), 400
