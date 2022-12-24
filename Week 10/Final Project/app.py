import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd, get_time, format_time, format_money

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd
app.jinja_env.filters["format_time"] = format_time
app.jinja_env.filters["format_money"] = format_money

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

"""
# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")
"""


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?",
                          request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure password was submitted again
        elif not request.form.get("confirmation"):
            return apology("must re-enter password", 400)

        # Ensure that the passwords match
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords don't match")

        # Check if the username is available
        check = db.execute(
            "SELECT * FROM users WHERE username=?", request.form.get("username"))
        if len(check) != 0:
            return apology("username not available")

        db.execute("INSERT INTO users (username, hash, cash) VALUES(?, ?, ?)",
                   request.form.get("username"), generate_password_hash(request.form.get("confirmation")), 10000.0)

        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/messages", methods=["GET", "POST"])
@login_required
def messages():
    """Send a message to another user"""
    if request.method == "POST":
        # Ensure something was submitted
        if not request.form.get("message"):
            return apology("must provide a message", 400)

        # Ensure recipient was submitted
        elif not request.form.get("recipient"):
            return apology("must provide a recipient", 400)

        # Check if the recipient exists
        check = db.execute(
            "SELECT * FROM users WHERE username=?", request.form.get("recipient"))
        if len(check) != 1:
            return apology("recipient does not exist")\

        # get last message id
        last_id = db.execute(
            "SELECT id FROM messages ORDER BY id DESC LIMIT 1")
        if last_id == []:
            last_id = [{"id": 0}]

        # Insert the message into the database
        db.execute("INSERT INTO messages (message, time, id) VALUES(?, ?, ?)",
                   request.form.get("message"), get_time(), last_id[0]["id"] + 1)
        db.execute("INSERT INTO message_info (message_id, sender, recipient) VALUES(?, ?, ?)",
                   last_id[0]["id"] + 1, session["user_id"], check[0]["id"])

        # say message sent
        flash("Message sent!")

        # refresh the page
        return redirect("/messages")

    else:
        # get all messages and the usernames of the senders including ones that the user sent
        messages = db.execute(
            "SELECT messages.message, messages.time, users.username FROM messages JOIN message_info ON messages.id = message_info.message_id JOIN users ON message_info.sender = users.id WHERE message_info.recipient = ? OR message_info.sender = ? ORDER BY messages.time DESC", session["user_id"], session["user_id"])
        return render_template("messages.html", messages=messages)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)
