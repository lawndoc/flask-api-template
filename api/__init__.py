from config import Config
from flask import Flask
from flask_restx import Api
import logging


# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)


# set logging options
level = [logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL][5-Config.LOG_LEVEL]
fmt = "%(asctime)s.%(msecs)03d %(levelname)-8s [%(name)s"
if Config.LOG_LEVEL == 5:  # debug
    fmt += ".%(funcName)s:%(lineno)d"
fmt += "] %(message)s"
logging.basicConfig(level=level,
                    format=fmt,
                    datefmt='%Y-%m-%dT%H:%M:%S')
log = logging.getLogger(Config.APP_NAME)


# import custom errors
from . import errors

# import namespaces
from .routes import api as api_ns

# initialize API
api = Api(title="Example API",
          version="1.0",
          description="Example API Template")
api.add_namespace(api_ns, path="/api")
api.init_app(app)
