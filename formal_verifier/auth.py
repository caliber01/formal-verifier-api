from flask_login import LoginManager
from flask import abort

from . import app
from .models import User

login_manager = LoginManager()


@login_manager.user_loader
def load_user(session_token):
    User.objects(session_token=session_token).first()


@login_manager.unauthorized_handler
def unauthorized():
    abort(401)


login_manager.init_app(app)
