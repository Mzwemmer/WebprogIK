from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
import smtplib, ssl
import random
import re

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
            return render_template("login.html", error="Provide a username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return render_template("login.html", error="Must provide password")

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return render_template("login.html", error="Username and/or Password incorrect")

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

        addressToVerify = request.form.get("email")
        match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', addressToVerify)

        # ensure username was submitted
        if not request.form.get("username"):
            return render_template("register.html", error="Provide an username.")

        # ensure password was submitted
        elif not request.form.get("password"):
            return render_template("register.html", error="Provide a password")

        # ensure the password was re-entered
        elif not request.form.get("confirmation"):
            return render_template("register.html", error="Correctly repeat your password.")

        elif not request.form.get("email"):
            return render_template("register.html", error="Provide an email adress.")

        elif "@" not in request.form.get("email"):
            return render_template("register.html", error="Provide a valid email adress.")

        elif match == None:
            return render_template("register.html", error="Provide a valid email adress")

        # raise an error if the password and username dont match
        if request.form.get("password") != request.form.get("confirmation"):
            return render_template("register.html", error="Correctly repeat your password.")

        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        check = check_register(username, email, password)

        if check == "Done":
            return redirect(url_for("login"))
        else:
            return render_template("register.html", error="Username/email has already been taken.")

    else:
        return render_template("register.html")


@app.route("/index", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":
        # check for the game that has a changed status so it can be added.
        number = str(0)
        jsonuser = session.get('jsonsession')
        for i in range(1, (len(jsonuser)+1)):
            temp_status = "status_" + str(i)
            game_addstatus = request.form.get(temp_status)
            if game_addstatus != "select":
                number = str(i)
                break

        temp_status = "status_" + str(number)
        temp_score = "rating_" + str(number)
        game_addrating = request.form.get(temp_score)
        game_addstatus = request.form.get(temp_status)

        # when the for loop fails this returns an erro to show the user that they need to input a status for the game.
        if game_addstatus == None:
            return render_template("index.html", json=jsonuser, error="Click on game info to input a status for the game you are trying to add.")

        # check if the added game got a rating from the user if no rating was found or a wrong rating
        # make the rating equeal to None.
        try:
            game_addrating = int(game_addrating)
            if game_addrating < 1 or game_addrating > 100:
                game_addrating = None
        except:
            game_addrating = None

        number = int(number)
        number -= 1

        # select the game and add it to the database.
        game_add = jsonuser[number]
        session_id = session["user_id"]
        addgame(game_add, session_id, game_addrating, game_addstatus)

        return redirect(url_for("allgames"))
    else:
        jsonuser = session.get('jsonsession')
        return render_template("index.html", json=jsonuser)


@app.route("/addgames", methods=["GET", "POST"])
@login_required
def addgames():
    if request.method == "POST":
        x = 1
        game_name = request.form.get("addgame")
        jsonuser = lookup(game_name)

        # add a counter and a summary to the games.
        for game in jsonuser:
            game["counter"] = x
            if 'rating' not in game:
                game["rating"] = "Rating unknown"
            if 'summary' not in game:
                game["summary"] = "No summary known"
            else:
                game["rating"] = str(game["rating"]).split('.')[0]
            x += 1

        session['jsonsession'] = jsonuser

        # catch a search that has no return if so raise an error.
        if lookup(game_name) == []:
            return render_template("addgames.html", error="The game you're looking for does not exist")

        return redirect(url_for("index"))
    else:
        return render_template("addgames.html")


@app.route("/allgames", methods=["GET", "POST"])
@login_required
def allgames():
    if request.method == "POST":
        user_id = session["user_id"]
        games = get_games(user_id, "*")

        # sort games if user selected rating or alphabetical. else sort by date
        if request.form.get("sortgames") == "rating":
            games = sortrating(user_id, "*")
            return render_template("allgames.html", games=games)
        elif request.form.get("sortgames") == "alfa":
            games = sortalfa(user_id, "*")
            return render_template("allgames.html", games=games)
        elif request.form.get("sortgames") == "date":
            return render_template("allgames.html", games=games)

        found = 0
        number = 0
        for i in range(1, (len(games)+1)):
            temp_status = "status_" + str(i)
            game_updatestatus = request.form.get(temp_status)
            if game_updatestatus != "select":
                number = i
                found = 1
                break

        for i in range(1, (len(games)+1)):
            if found == 1:
                break
            temp_rating = "rating_" + str(i)
            game_updaterating = request.form.get(temp_rating)
            if game_updaterating:
                number = i
                found = 1
                break

        if found == 1:
            temp_rating = "rating_" + str(number)
            game_updaterating = request.form.get(temp_rating)

        try:
            game_updaterating = int(game_updaterating)
            if game_updaterating < 1 or game_updaterating > 100:
                game_addrating = None
        except:
            game_updaterating = None

        number = int(number)
        number -= 1
        if found == 0:
            return render_template("allgames.html", games=games, error="No game found that is supposed to be updated.")

        # select the game and update it in the database.
        game = games[number]
        update = update_game(user_id, game, game_updatestatus, game_updaterating)

        games = get_games(user_id, "*")
        if update == "Done":
            return render_template("allgames.html", games=games)

        games = get_games(user_id, "*")
        return render_template("allgames.html", games=games, error="Oops something went wrong.")
    else:
        user_id = session["user_id"]
        games = get_games(user_id, "*")
        return render_template("allgames.html", games=games)


@app.route("/completed", methods=["GET", "POST"])
@login_required
def completed():
    user_id = session["user_id"]
    games = get_games(user_id, "completed")

    if request.method == "POST":
        # sort games if user selected rating or alphabetical. else sort by date
        if request.form.get("sortgames") == "rating":
            games = sortrating(user_id, "completed")
            return render_template("completed.html", games=games)
        elif request.form.get("sortgames") == "alfa":
            games = sortalfa(user_id, "completed")
            return render_template("completed.html", games=games)
        elif request.form.get("sortgames") == "date":
            return render_template("completed.html", games=games)

    else:
        return render_template("completed.html", games=games)


@app.route("/currently", methods=["GET", "POST"])
@login_required
def currently():
    user_id = session["user_id"]
    games = get_games(user_id, "current")

    if request.method == "POST":
        # sort games if user selected rating or alphabetical. else sort by date
        if request.form.get("sortgames") == "rating":
            games = sortrating(user_id, "currently")
            return render_template("currently.html", games=games)
        elif request.form.get("sortgames") == "alfa":
            games = sortalfa(user_id, "currently")
            return render_template("currently.html", games=games)
        elif request.form.get("sortgames") == "date":
            return render_template("currently.html", games=games)
    else:
        return render_template("currently.html", games=games)


@app.route("/dropped", methods=["GET", "POST"])
@login_required
def dropped():
    user_id = session["user_id"]
    games = get_games(user_id, "dropped")

    if request.method == "POST":
        # sort games if user selected rating or alphabetical. else sort by date
        if request.form.get("sortgames") == "rating":
            games = sortrating(user_id, "dropped")
            return render_template("dropped.html", games=games)
        elif request.form.get("sortgames") == "alfa":
            games = sortalfa(user_id, "dropped")
            return render_template("dropped.html", games=games)
        else:
            return render_template("dropped.html", games=games)
    else:
        return render_template("currently.html", games=games)


@app.route("/onhold", methods=["GET", "POST"])
@login_required
def onhold():
    user_id = session["user_id"]
    games = get_games(user_id, "hold")

    if request.method == "POST":
        # sort games if user selected rating or alphabetical. else sort by date
        if request.form.get("sortgames") == "rating":
            games = sortrating(user_id, "onhold")
            return render_template("onhold.html", games=games)
        elif request.form.get("sortgames") == "alfa":
            games = sortalfa(user_id, "onhold")
            return render_template("onhold.html", games=games)
        else:
            return render_template("onhold.html", games=games)
    else:
        return render_template("currently.html", games=games)


@app.route("/wishlist", methods=["GET", "POST"])
@login_required
def wishlist():
    user_id = session["user_id"]
    games = get_games(user_id, "wishlist")

    if request.method == "POST":
        # sort games if user selected rating or alphabetical. else sort by date
        if request.form.get("wishlist") == "rating":
            games = sortrating(user_id, "wishlist")
            return render_template("wishlist.html", games=games)
        elif request.form.get("sortgames") == "alfa":
            games = sortalfa(user_id, "wishlist")
            return render_template("wishlist.html", games=games)
        else:
            return render_template("wishlist.html", games=games)
    else:
        return render_template("currently.html", games=games)


@app.route("/forgotpasw", methods=["GET", "POST"])
def forgotpasw():
    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        if not request.form.get("username"):
            return render_template("forgotpasw.html", error="Provide a username")

        # ensure password was submitted
        elif not request.form.get("email"):
            return render_template("forgotpasw.html", error="provide an e-mail adress")

        # send an email to the user with a code
        username = request.form.get("username")
        email = request.form.get("email")
        valid = check(email, username)
        if valid == None:
            return render_template("forgotpasw.html", error="Invalid email/username combination.")
        else:
            item = code(code)
            port = 465  # For SSL
            smtp_server = "smtp.gmail.com"
            sender_email = "inmaticauser1@gmail.com"  # Enter your address
            receiver_email = request.form.get("email")  # Enter receiver address
            password = "maticain"
            message = """\

            If you did not do this, ignore this mail and/or block this adress.

            For changing your password/email-adress;
            Enter the following code on the In-Matica page: """ + str(item)

            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message)

        return render_template("send.html", error="A code has been send to your e-mail adress")
    else:
        return render_template("forgotpasw.html")


@app.route("/send", methods=["GET", "POST"])
def send():
    if request.method == "POST":
        if not request.form.get("username"):
            return render_template("send.html", error="Enter the username connected to your account")
        elif not request.form.get("newpas"):
            return render_template("send.html", error="Provide a new password")
        elif not request.form.get("newpas2"):
            return render_template("send.html", error="Verify the password")
        elif not request.form.get("code"):
            username = request.form.get("username")
            delete2(username)
            return render_template("forgotpasw.html", error="Invalid code")
        elif request.form.get("newpas") != request.form.get("newpas2"):
            return render_template("send.html", error="Passwords do not match")

        # make sure a valid password was provided and a valid code aswell
        newpassword = request.form.get("newpas")
        username = request.form.get("username")
        code = request.form.get("code")
        if update_password(newpassword, username, code) == None:
            username = request.form.get("username")
            delete2(username)
            return render_template("forgotpasw.html", error="Invalid code")
        else:
            username = request.form.get("username")
            delete2(username)
            return render_template("login.html")
    return render_template("send.html")


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    if request.method == "POST":

        # check if either change password or another option is selected
        user_id = session["user_id"]
        if not request.form.get("new_pass") and not request.form.get("check_pass"):
            what = request.form.get("select")
            new = request.form.get("new")
            check = request.form.get("check")
        else:
            what = "password"
            new = request.form.get("new_pass")
            check = request.form.get("check_pass")

        if what == "select":
            return render_template("account.html", error="Please select what you want to change.")

        if new != check:
            return render_template("account.html", error="Please repeat your input correctly.")

        check = change(user_id, what, new)
        if check == "Done":
            return render_template("account.html")
        else:
            return render_template("account.html", error="Username/email has already been taken.")

        return render_template("account.html")
    else:
        return render_template("account.html")


@app.route("/delete", methods=["GET", "POST"])
@login_required
def delete():
    # run a script that deletes the account. This page is a page inbetween 2 pages and reders nothing.
    user_id = session["user_id"]
    delete_account(user_id)

    return redirect(url_for("login"))


@app.route("/deletegame", methods=["GET", "POST"])
@login_required
def deletegame():
    user_id = session["user_id"]
    games = get_games(user_id, "*")

    # run script that deletes game. page renders back to allgames
    for game in games:
        gamename = game["name"]

    remove_game(gamename, user_id)

    return redirect(url_for("allgames"))


@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))


@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
    if request.method == "POST":
        username = request.form.get("namesearch")
        name = lookup_name(username)
        status = request.form.get("status")
        if name == None:
            return render_template("search.html", error="Username not found in the system")
        else:
            name = name[0]
            games = get_games(name["id"], status)
            if status == "*":
                status = "all games"
            return render_template("found.html", games=games, name=username, status=status)
    else:
        return render_template("search.html")


@app.route("/tip", methods=["GET", "POST"])
@login_required
def tip():
    if request.method == "POST":
        to_tip_name = request.form.get("name")
        to_tip_game = request.form.get("game_tip")

        user_id = session["user_id"]
        games = get_tips(user_id)

        # input the tip into the database
        tip = tip_input(user_id, to_tip_game, to_tip_name)
        json = get_games(user_id, "*")

        if tip == None:
            return render_template("tips.html", games=games, json=json, error="No user found for the tip to go to.")
        else:
            return render_template("tips.html", games=games, json=json)
    else:
        user_id = session["user_id"]
        games = get_tips(user_id)
        json = get_games(user_id, "*")
        return render_template("tips.html", games=games, json=json)


@app.route("/found", methods=["GET", "POST"])
def found():
    return render_template("found.html")
