import re

from coinvibes import app

def remove_non_ascii(s):
    return "".join(filter(lambda x: ord(x)<128, s))

def remove_non_numeric(s):
    return re.sub("[^0-9.]", "", s)

class APIError(Exception):
    status_code = 500

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

from functools import wraps
from flask import request
import analytics

def identify_user(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = request.remote_addr
        analytics.identify(user_id, {})
        return f(*args, **kwargs)
    return decorated_function

# Heroku Request

from flask import Request
 
class HerokuRequest(Request):
    """
    `Request` subclass that overrides `remote_addr` with Heroku's
    HTTP_X_FORWARDED_FOR when available.
    """
 
    @property
    def remote_addr(self):
        """The remote address of the client."""
        fwd = self.environ.get('HTTP_X_FORWARDED_FOR', None)
        if fwd is None:
            return self.environ.get('REMOTE_ADDR')
        # sometimes x-forwarded-for contains multiple addresses,
        # actual client is first, rest are proxy
        fwd = fwd.split(',')[0]
        return fwd
