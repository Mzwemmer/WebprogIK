import csv
import urllib.request
import json
import requests
from flask import redirect, render_template, request, session
from functools import wraps
from cs50 import SQL
from passlib.apps import custom_app_context as pwd_context
import smtplib
import random

db = SQL("sqlite:///games.db")

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
    url = 'https://api-v3.igdb.com/games/'
    headers = {'user-key': '663bdc9cdfcbb5aaae5a2a8a14b4d70a'}
    data = f'search "{name}"; fields name, rating, summary;'
    r = requests.get(url, headers = headers, json = {"key":"value"}, data = data)
    if not r:
        return None
    return r.json()

def delete_account(user_id):
    db.execute("DELETE FROM users WHERE id =:id", id = user_id)
    return "Done"

def check_register(username, email, password):
    temp_email = db.execute("SELECT * FROM users WHERE email=:email", email=email)
    temp_username = db.execute("SELECT * FROM users WHERE username=:username", username = username)
    if len(temp_email) == 1:
        return render_template("register.html")
    elif len(temp_username) == 1:
        return render_template("register.html")
    else:
        newUser = db.execute("INSERT INTO users (username, hash, email) VALUES (:username, :hash, :email)",
                             username=username, hash=pwd_context.hash(password), email = email)

    return "Done"

def addgame(game,user_id,rating,status):
    temp = db.execute("SELECT * FROM games WHERE user_id=:user_id AND name=:name", user_id=user_id, name=game["name"])
    if temp:
        return "error"
    else:
        db.execute("INSERT INTO games (name, rating, user_id, status, userrating) VALUES (:name, :rating, :user_id, :status, :userrating)",
                    name=game["name"], rating=game["rating"], user_id=user_id, status=status, userrating=rating)


def get_games(user_id,status):
    if status == "*":
        games = db.execute("SELECT * FROM games WHERE user_id=:user_id", user_id = user_id)
    else:
        games = db.execute("SELECT * FROM games WHERE user_id=:user_id AND status=:status", user_id = user_id, status = status)

    i = 1
    for game in games:
        game["rating"] = str(game["rating"]).split('.')[0]
        game["counter"] = i
        i += 1
    return games

def update_game(user_id, game, status, rating):
    to_update = game["name"]
    if rating == None:
        rating = db.execute("SELECT rating FROM games WHERE user_id=:user_id AND name=:name", user_id=user_id, name=to_update)

    if status == None:
        status = db.execute("SELECT status FROM games WHERE user_id=:user_id AND name=:name", user_id=user_id, name=to_update)

    selected_game = db.execute("UPDATE games(status,rating;) VALUES (:status,:rating", status=status,rating=rating)

    return "Done"

def remove_game(name, user_id):
    db.execute("DELETE FROM games WHERE name=:name AND user_id=:user_id", name=name, user_id=user_id)

def lookup_name(name):
    temp = db.execute("SELECT id FROM users WHERE username=:username", username=name)
    if temp == []:
        return None
    else:
        return temp

def sortrating(user_id,status):
    if status == "*":
        games = db.execute("SELECT * FROM games WHERE user_id=:user_id ORDER BY userrating DESC", user_id = user_id)
    else:
        games = db.execute("SELECT * FROM games WHERE user_id=:user_id AND status=:status ORDER BY userrating DESC", user_id = user_id, status = status)

    i = 1
    for game in games:
        game["rating"] = str(game["rating"]).split('.')[0]
        game["counter"] = i
        i += 1

    return games

def sortalfa(user_id,status):
    if status == "*":
        games = db.execute("SELECT * FROM games WHERE user_id=:user_id ORDER BY name ASC", user_id = user_id)
    else:
        games = db.execute("SELECT * FROM games WHERE user_id=:user_id AND status=:status ORDER BY name ASC", user_id = user_id, status = status)

    i = 1
    for game in games:
        game["rating"] = str(game["rating"]).split('.')[0]
        game["counter"] = i
        i += 1

    return games

def check(email,username):
    valid = db.execute("SELECT email FROM users WHERE username=:username", username=username)
    valid = valid[0]["email"]
    if valid != email:
        return None
    else:
        return "Done"

def code(code):
    code = random.randint(1000000,100000000)
    db.execute("UPDATE users SET code= :code WHERE username=:username and email=:email", code=code, username= request.form.get("username"), email=request.form.get("email"))
    return code

def delete():
    code = db.execute("SELECT code FROM users WHERE username=:username", username=request.form.get("username"))
    db.execute("DELETE FROM users WHERE code=:code ", code=code)

def update_password(newpassword,username,code):
    if code != db.execute("SELECT code FROM users WHERE username=:username", username=request.form.get("username")):
        return None
    else:
        db.execute("UPDATE users SET hash=:hash WHERE username=:username", hash=pwd_context.hash(newpassword), username=username)
