from functools import wraps
from flask import session

def login_is_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            kwargs['status'] = "loggedout"  # Authorization required
            return function(*args, **kwargs)
        else:
            email = session["email"]
            print(session)
            return function(*args, **kwargs)
    return wrapper