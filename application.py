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
            return render_template("login.html", error = "Provide a username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return render_template("login.html", error = "Must provide password")

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return render_template("login.html", error = "Username and/or Password incorrect")

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
            return render_template("register.html", error = "Provide an username.")

        # ensure password was submitted
        elif not request.form.get("password"):
            return render_template("register.html", error = "Provide a password")

        # ensure the password was re-entered
        elif not request.form.get("confirmation"):
            return render_template("register.html", error = "Correctly repeat your password.")

        elif not request.form.get("email"):
            return render_template("register.html", error = "Provide an email adress.")

        elif "@" not in request.form.get("email"):
            return render_template("register.html", error = "Provide a valid email adress.")

        # raise an error if the password and username dont match
        if request.form.get("password") != request.form.get("confirmation"):
            return render_template("register.html", error = "Correctly repeat your password.")

        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        check = check_register(username, email, password)

        if check == "Done":
            return redirect(url_for("login"))
        else:
            return render_template("register.html", error = "Oops something went wrong.")

    else:
        return render_template("register.html")


@app.route("/index", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":
        number = str(0)
        jsonuser = session.get('jsonsession')
        for i in range(1,(len(jsonuser)+1)):
            temp_status = "status_" + str(i)
            game_addstatus = request.form.get(temp_status)
            if game_addstatus != "select":
                number = str(i)
                break

        temp_status = "status_" + str(number)
        temp_score = "rating_" + str(number)
        game_addrating = request.form.get(temp_score)
        game_addstatus = request.form.get(temp_status)
        if game_addstatus == None:
            return render_template("index.html", json=jsonuser, error = "Click on game info to input a status for the game you are trying to add.")
        try:
            game_addrating = int(game_addrating)
            if game_addrating < 1 or game_addrating > 100:
                game_addrating = None
        except:
            game_addrating = None

        number = int(number)
        number -=1

        game_add = jsonuser[number]
        session_id = session["user_id"]
        addgame(game_add,session_id,game_addrating,game_addstatus)

        return redirect(url_for("allgames"))
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
            if 'summary' not in game:
                game["summary"] = "No summary known"
            x+=1

        session['jsonsession'] = jsonuser

        if lookup(game_name) == []:
            return render_template("addgames.html", error = "The game you're looking for does not exist")

        return redirect(url_for("index"))
    else:
        return render_template("addgames.html")
@app.route("/allgames", methods=["GET", "POST"])
@login_required
def allgames():
    user_id = session["user_id"]
    games = get_games(user_id, "*")

    if len(games) != 0:
        return render_template("allgames.html", games = games)

    else:
        message = "No games added yet. Click add games in the top left corner"
        return render_template("allgames.html", message = message)

@app.route("/completed", methods=["GET", "POST"])
@login_required
def completed():
    user_id = session["user_id"]
    games = get_games(user_id, "completed")

    return render_template("completed.html", games = games)

@app.route("/currently", methods=["GET", "POST"])
@login_required
def currently():
    user_id = session["user_id"]
    games = get_games(user_id, "current")

    return render_template("currently.html", games = games)

@app.route("/dropped", methods=["GET", "POST"])
@login_required
def dropped():
    user_id = session["user_id"]
    games = get_games(user_id,"dropped")

    return render_template("dropped.html", games = games)

@app.route("/onhold", methods=["GET", "POST"])
@login_required
def onhold():
    user_id = session["user_id"]
    games = get_games(user_id, "hold")

    return render_template("onhold.html", games = games)

@app.route("/wishlist", methods=["GET", "POST"])
@login_required
def wishlist():
    user_id = session["user_id"]
    games = get_games(user_id, "wishlist")

    return render_template("wishlist.html", games = games)

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

@app.route("/account", methods=["GET", "POST"])
@login_required
def account():

    return render_template("account.html")

@app.route("/delete", methods=["GET", "POST"])
@login_required
def delete():
    user_id = session["user_id"]
    delete_account(user_id)

    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))
