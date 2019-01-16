from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
import unicodedata

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
db = SQL("sqlite:///PicUs.db")

@app.route("/")
def index():
    """The index of the website"""
    if request.method == "POST":
        return "hoi"
    else:
        return render_template("index.html")

#GINO
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # checken voor goede invulling
        if not request.form.get("email"):
            return "jammer neef"
        if not request.form.get("username"):
            return "jammer neef"
        if request.form.get("password") != request.form.get("confirmation"):
            return "jammer neef"
        if request.form.get("password") == "":
            return "jammer neef"
        elif not request.form.get("password"):
            return "jammer neef"
        elif not request.form.get("confirmation"):
            return "jammer neef"

        geregistreerd = db.execute("INSERT INTO users (email, username, hash) VALUES(:email, :username, :password)", email=request.form.get("email"), username=request.form.get("username"), password=pwd_context.hash(request.form.get("password")))

        if not geregistreerd:
            return apology("Helaas")

        # gebruiker onthouden
        session["user_id"] = geregistreerd

        # als alles doorstaan en voltooid is, bevestig registratie
        return redirect(url_for("groupfeed"))

    # opnieuw registerpagina tevoorschijn toveren wanneer geen POST
    else:
        return render_template("register.html")

@app.route("/makegroup", methods=["GET", "POST"])
@login_required
def makegroup():
    """Make new group"""
    if request.method == "POST":
        count = request.form.get("count_member")

        return render_template("addgroupmember.html", count=count)
    else:
        return render_template("makegroup.html")

@app.route("/addmember", methods=["GET", "POST"])
@login_required
def addmember():
    if request.method == "POST":

        name_group = request.form.get("name_group")
        count = request.form.get("count_member")

        for number in range(len(count)):
            add_members = request.form.get(number)

            user = find_user(add_members)
            if user == []:
                return "Username doesn't exist"

            db.execute("INSERT INTO groups (groupname, username) VALUES(:groupname, :username)", groupname=name_group, username=add_members)
        return render_template("addgroupmember.html", count=count)
    else:
        return render_template("addgroupmember.html")

@app.route("/eventview", methods=["GET", "POST"])
def eventview():
    if request.method == "POST":
        return "hoi"
    else:
        return render_template("eventview.html")

@app.route("/makeevent", methods=["GET", "POST"])
@login_required
def makeevent():
    if request.method == "POST":
        if not request.form.get("makeevent"):
            return "inset eventname"

        return render_template("aboutus")
        if len(db.execute("SELECT * FROM event WHERE event=:event", event=request.form.get("makeevent"))) > 0:
            return apology("eventname already exists")

    else:
        return render_template("makeevent")



#GINO
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # Als POST kan
    if request.method == "POST":

        # username verzekeren
        if not request.form.get("username"):
            return "must provide username"

        # wachtwoord verzekeren
        elif not request.form.get("password"):
            return "must provide password"

        # username database
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # kijken of username uniek is en wachtwoord klopt
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return "invalid username and/or password"

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # redirect user to home page

        return redirect(url_for("groupfeed"))
    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/groupfeed", methods=["GET", "POST"])
def groupfeed():
    return render_template("groupfeed.html")

@app.route("/aboutus", methods=["GET", "POST"])
def aboutus():
    return render_template("aboutus.html")