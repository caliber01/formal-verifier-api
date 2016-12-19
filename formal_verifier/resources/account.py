from flask import request, abort
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from bson.json_util import dumps

from formal_verifier import app, bcrypt
from formal_verifier.mappers import map_user_to_view_model
from formal_verifier.models import User


@app.route('/login', methods=['POST'])
def login():
    json = request.get_json()
    username = json['username']
    password = json['password']
    user = User.objects(username=username).first()
    if bcrypt.check_password_hash(user.password_hash, password):
        response = {
            'access_token': create_access_token(identity=username),
            'user': map_user_to_view_model(user)
        }
        return dumps(response)
    else:
        abort(401)


@app.route('/register', methods=['POST'])
def register():
    json = request.get_json()
    fields = {key: value for (key, value) in json.items() if key in User._fields}
    user = User(**fields)
    user.password_hash = bcrypt.generate_password_hash(json['password'])
    user.is_active = True
    user.save()
    response = {
        'access_token': create_access_token(identity=user.username),
        'user': map_user_to_view_model(user)
    }
    return dumps(response)


@app.route('/account', methods=['GET'])
@jwt_required
def account():
    app.logger.info(get_jwt_identity())
    return User.objects(username=get_jwt_identity()).first().to_json()
