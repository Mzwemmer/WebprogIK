from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp

from helpers import *

# configure application
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response


# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///games.db")

@app.route("/", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return apology("invalid username and/or password")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""
    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # ensure the password was re-entered
        elif not request.form.get("confirmation"):
            return apology("must provide confirmation")

        # raise an error if the password and username dont match
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("the passwords don't match")

        #hash the password and enter it in the database
        userlistdict = db.execute("SELECT username FROM users")
        userlist = []
        for userdict in userlistdict:
            for x in userdict:
                userlist.append(userdict[x])

        if request.form.get("username") in userlist:
            return apology("username already taken")

        rows = db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)", username=request.form.get("username"),  hash=pwd_context.hash(request.form.get("password")))


        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # redirect user to home page
        return redirect(url_for("index"))


    else:
        return render_template("register.html")

@app.route("/index", methods=["GET", "POST"])
@login_required
def index():
    return render_template("index.html")

@app.route("/allgames", methods=["GET", "POST"])
@login_required
def allgames():
    return render_template("allgames.html")

@app.route("/completed", methods=["GET", "POST"])
@login_required
def completed():
    return render_template("completed.html")

@app.route("/currently", methods=["GET", "POST"])
@login_required
def currently():
    return render_template("currently.html")

@app.route("/dropped", methods=["GET", "POST"])
@login_required
def dropped():
    return render_template("dropped.html")

@app.route("/onhold", methods=["GET", "POST"])
@login_required
def onhold():
    return render_template("onhold.html")

@app.route("/whishlist", methods=["GET", "POST"])
@login_required
def whishlist():
    return render_template("whishlist.html")



@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))
