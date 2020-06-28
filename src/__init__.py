from flask import Flask, g
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api, marshal_with
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

import logging.config

app = Flask(__name__)
app.config.from_object("src.config.Config")
# db
db = SQLAlchemy(app)
# migrate
migrate = Migrate(app, db)
# ma
ma = Marshmallow()
# routes
routes = Api(app)
# cors
CORS(app)
# logging
logging.config.dictConfig(app.config['LOGGING_CONFIG'])

# import models
from .models import *

# import resources
from .resources.v1 import (Login, Logout, Ping, Register, Status)

# import common
from .common import (
    ManualException,
    ErrorResponse,
    RoleEnum,
    StatusEnum
)

routes.add_resource(Login, '/login', methods=['POST'])
routes.add_resource(Logout, '/logout', methods=['POST'])
routes.add_resource(Ping, '/ping', methods=['GET'])
routes.add_resource(Register, '/register', methods=['POST'])
routes.add_resource(Status, '/status', methods=['GET'])

if app.config['ENV'] == 'development':
    # error handling
    @app.errorhandler(Exception)
    @marshal_with(ErrorResponse.marshallable())
    def handle_error(error):
        return ErrorResponse()


    @app.errorhandler(ManualException)
    @marshal_with(ErrorResponse.marshallable())
    def handle_manual_error(error):
        return ErrorResponse(code=error.code, msg=error.msg)


# before each request
@app.before_request
def handle_request():
    g.logger = logging
    g.db = db
    g.config = app.config
