import logging.config

from flask import Flask
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restful import Api, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object("src.config.Config")
# cache
# cache = Cache(app, config=app.config['REDIS_CONFIG'])
cache = None
# cors
CORS(app, supports_credentials=True)
# db
db = SQLAlchemy(app)
# migrate
migrate = Migrate(app, db)
# ma
ma = Marshmallow()
# routes
api = Api(app)

# logging
logging.config.dictConfig(app.config['LOGGING_CONFIG'])

# import models
from .models import *
# import routes
from .routes import *

# import common
from .common import (
    ManualException,
    ErrorResponse
)

if app.config['ENV'] != 'development':
    # error handling
    @app.errorhandler(Exception)
    @marshal_with(ErrorResponse.marshallable())
    def handle_error(error):
        return ErrorResponse(), 500


    @app.errorhandler(ManualException)
    @marshal_with(ErrorResponse.marshallable())
    def handle_manual_error(error):
        return ErrorResponse(code=error.code, msg=error.msg), error.code

# import libs
from .libs import *
from .event import new_event_listener

consumer = Consumer(url=app.config['KAFKA_URL'],
                    topics=app.config['KAFKA_TOPICS'], event_listener=new_event_listener)


@app.before_first_request
def func():
    consumer.start()
