from flask import flash, redirect, url_for, session
from functools import wraps

def is_authenticated(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("Unauthorized. Login first", "danger")
            return redirect(url_for("auth.login"))

    return wrap
