
from base64 import b64decode


from skipole import FailPage, GoTo, ValidateError, ServerError

from .. import database_ops


def check_login(environ):
    "Returns True if login ok, False otherwise"
    try:
        access_user = database_ops.get_access_user()
        access_password, seed = database_ops.get_password(access_user)
        # access_password is the hashed password stored in the database
        if not access_password:
            return False
        auth = environ.get('HTTP_AUTHORIZATION')
        if auth:
            scheme, data = auth.split(" ", 1)
            if scheme.lower() != 'basic':
                return False
            username, password = b64decode(data).decode('UTF-8').split(':', 1)
            if username != access_user:
                return False
            hashed_password, seed = database_ops.hash_password(password, seed)
            if hashed_password == access_password:
                # login ok
                return True
    except:
        pass
        # Any exception causes False to be returned
    # login fail
    return False


def check_password(password):
    "Returns True if password ok, False otherwise"
    try:
        access_user = database_ops.get_access_user()
        database_password, seed = database_ops.get_password(access_user)
        if (database_password, seed) == database_ops.hash_password(password, seed):
            # password ok
            return True
    except:
        pass
        # Any exception causes False to be returned
    # password fail
    return False



def request_login(skicall):
    """Set up the basic authentication"""
    realm = 'Basic realm="' + skicall.project + '"'
    skicall.page_data['headers'] = [
            ('content-type', 'text/html'),
            ('WWW-Authenticate', realm)]
    skicall.page_data['status'] = '401 Unauthorized'

