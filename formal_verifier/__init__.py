from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask("formal_verifier")
bcrypt = Bcrypt(app)

app.secret_key = b'\x1e2\xeb\x0f\xe1\xd2Z\xdb\xcf4\xd0\xbc\x7fq,c\xc1\xdf\x18L\xf3\xcd\x8d\xef'

import formal_verifier.auth
import formal_verifier.models
import formal_verifier.errorhandler
import formal_verifier.controllers

