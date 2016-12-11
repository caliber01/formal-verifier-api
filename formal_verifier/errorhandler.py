from mongoengine import ValidationError, NotUniqueError

from . import app


@app.errorhandler(401)
def handle_401(error):
    app.logger.error(error)
    return 'Unauthorized', 401, {'WWWAuthenticate': 'Basic realm="Login Required"'}


@app.errorhandler(400)
def handle_400(error):
    app.logger.info(type(error))
    app.logger.error(error)
    return 'Bad request', 400


for errorType in [ValidationError, NotUniqueError]:
    @app.errorhandler(errorType)
    def handle_validation_error(error):
        app.logger.error(error)
        return 'Bad request', 400
