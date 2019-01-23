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
            return render_template("login")

        # ensure password was submitted
        elif not request.form.get("password"):
            return render_template("login")

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return render_template("login")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # redirect user to home page
        return redirect(url_for("allgames"))

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
            return render_template("register.html")

        # ensure password was submitted
        elif not request.form.get("password"):
            return render_template("register.html")

        # ensure the password was re-entered
        elif not request.form.get("confirmation"):
            return render_template("register.html")

        elif not request.form.get("email"):
            return render_template("register.html")

        elif "@" not in request.form.get("email"):
            return render_template("register.html")

        # raise an error if the password and username dont match
        if request.form.get("password") != request.form.get("confirmation"):
            returnrender_template("register.html")

        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        check = check_register(username, email, password)

        if check == "Done":
            return redirect(url_for("login"))
        else:
            return render_template("register.html")

    else:
        return render_template("register.html")

@app.route("/index", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":
        game_addnumber = int(request.form.get("number"))

        if game_addnumber < 1 or game_addnumber > 10:
            return render_template("index.html")

        jsonuser = session.get('jsonsession')
        game_add = jsonuser[game_addnumber]
        session_id = session.get(session["user_id"])
        addgame(game_add,session_id)
        return render_template("index.html")
    else:
        jsonuser = session.get('jsonsession')
        return render_template("index.html", json = jsonuser)

@app.route("/addgames", methods=["GET","POST"])
@login_required
def addgames():
    if request.method == "POST":
        x=1
        game_name = request.form.get("addgame")
        jsonuser = lookup(game_name)

        for game in jsonuser:
            game["counter"] = x
            if 'rating' not in game:
                game["rating"] = "Rating unknown"
            x+=1

        session['jsonsession'] = jsonuser

        return redirect(url_for("index"))
    else:
        return render_template("addgames.html")

@app.route("/allgames", methods=["GET", "POST"])
@login_required
def allgames():
    user_id = session["user_id"]
    games = get_allgames(user_id)

    i= 1
    for game in games:
        game["number"] = i
        i += 1

    return render_template("allgames.html", games = games)
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

@app.route("/wishlist", methods=["GET", "POST"])
@login_required
def wishlist():
    return render_template("wishlist.html")

@app.route("/forgotpasw", methods=["GET", "POST"])
def forgotpasw():
    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # ensure username was submitted
        if not request.form.get("username"):
            return render_template("forgotpasw.html")

        # ensure password was submitted
        elif not request.form.get("email"):
            return render_template("forgotpasw.html")

        return render_template("send.html")
    else:
        return render_template("forgotpasw.html")

@app.route("/send", methods=["GET", "POST"])
def send():
    return render_template("send.html")


@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))
