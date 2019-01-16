import csv
import urllib.request
import json
import requests

from flask import redirect, render_template, request, session
from functools import wraps


def apology(message, code=400):
    """Renders message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function




def lookup(name):
    name = name
    url = 'https://api-v3.igdb.com/games/'
    headers = {'user-key': '663bdc9cdfcbb5aaae5a2a8a14b4d70a'}
    data = f'search "{name}"; fields name, rating;'
    r = requests.get(url, headers = headers, json = {"key":"value"}, data = data)
    if r == []:
        return None
    return r.json()
