from mongoengine import ValidationError

from . import app


@app.errorhandler(401)
def handle_401(error):
    return 'Unauthorized', 401, {'WWWAuthenticate': 'Basic realm="Login Required"'}


# @app.errorhandler(ValidationError)
# def handle_validation_error(error):
    # return 'Bad request', 400
