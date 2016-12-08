from flask import request, abort, jsonify
from flask_login import login_required, logout_user, login_user, current_user

from formal_verifier import app, bcrypt
from formal_verifier.models import User


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = User.objects(username=username).first()
    if bcrypt.check_password_hash(user.password_hash, password):
        login_user(user)
        return jsonify(success=True)
    else:
        abort(401)


@app.route('/register', methods=['POST'])
def register():
    fields = {key: request.form[key] for key in request.form if key in User.get_field_names()}
    user = User(**fields)
    user.password_hash = bcrypt.generate_password_hash(request.form['password'])
    app.logger.info(type(user.password_hash))
    user.is_active = True
    user.save()
    return user.to_json()


@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()


@app.route('/account', methods=['GET'])
@login_required
def account():
    return current_user
