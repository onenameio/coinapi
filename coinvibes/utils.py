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
 
class ProxiedRequest(Request):
    """
    `Request` subclass that overrides `remote_addr` with Frontend Server's
    HTTP_X_FORWARDED_FOR when available.
    """
 
    @property
    def remote_addr(self):
        """The remote address of the client."""
        # Get a parsed version of X-Forwarded-For header (contains 
        #    REMOTE_ADDR if no forwarded-for header). See
        #    http://en.wikipedia.org/wiki/X-Forwarded-For
        fwd = self.access_route
        remote = self.environ.get('REMOTE_ADDR', None)
        if fwd and self._is_private_ip(remote):
            # access route is a list where the client is first
            # followed by any intermediary proxies. However, we 
            # can only trust the last entry as valid -- it's from
            # the server one hop behind the one connecting.
            return fwd[-1]
        else:
            return remote
 
    def _is_private_ip(self,ip):
        blank_ip = (ip is None or ip == '')
        private_ip = (ip.startswith('10.') or ip.startswith('172.16.') or ip.startswith('192.168.'))
        local_ip = (ip == '127.0.0.1' or ip == '0.0.0.0')
        return blank_ip or private_ip or local_ip