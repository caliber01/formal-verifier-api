from flask import request, abort, jsonify
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from bson.json_util import dumps

from formal_verifier import app, bcrypt
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
            'user': user.to_mongo()
        }
        return dumps(response)
    else:
        abort(401)


@app.route('/register', methods=['POST'])
def register():
    json = request.get_json()
    fields = {key: json[key] for key in json if key in User.get_field_names()}
    user = User(**fields)
    user.password_hash = bcrypt.generate_password_hash(json['password'])
    user.is_active = True
    user.save()
    return user.to_json()


@app.route('/account', methods=['GET'])
@jwt_required
def account():
    app.logger.info(get_jwt_identity())
    return User.objects(username=get_jwt_identity()).first().to_json()
