from flask import Flask, Response
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api


class CustomResponse(Response):
    default_mimetype = 'application/json'


class CustomFlask(Flask):
    response_class = CustomResponse

app = CustomFlask("formal_verifier")
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
api = Api(app)
CORS(app)

app.secret_key = b'\x1e2\xeb\x0f\xe1\xd2Z\xdb\xcf4\xd0\xbc\x7fq,c\xc1\xdf\x18L\xf3\xcd\x8d\xef'

import formal_verifier.encoding
import formal_verifier.models
import formal_verifier.errorhandler
import formal_verifier.resources

