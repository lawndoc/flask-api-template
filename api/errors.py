from api import app, log
import json
from werkzeug.exceptions import InternalServerError, NotFound


class CustomError(Exception):
    """ Base class for all exceptions in this module. """
    pass


@app.errorhandler(InternalServerError)
def handle_500(error):
    """ Return JSON instead of HTML for 500 errors. """
    response = error.get_response()
    response.data = json.dumps({
        "code": error.code,
        "name": error.name,
        "description": error.description})
    log.error(response.data)
    response.content_type = "application/json"
    return response, 500


@app.errorhandler(NotFound)
def handle_404(error):
    """ Return JSON instead of HTML for 404 errors. """
    response = error.get_response()
    response.data = json.dumps({
        "code": error.code,
        "name": error.name,
        "description": error.description})
    response.content_type = "application/json"
    return response, 404