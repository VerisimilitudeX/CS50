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

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    totalBalance = balance = db.execute(
        "SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]
    portfolio = db.execute(
        "SELECT symbol, SUM(quantity) FROM transactions WHERE u_id=? GROUP BY symbol", session["user_id"])
    prices = []

    for i, owned in enumerate(portfolio):
        temp = lookup(owned["symbol"])["price"]
        prices.append(temp)
        totalBalance += portfolio[i]["SUM(quantity)"] * prices[i]

    return render_template("index.html", port=portfolio, prices=prices, balance=balance, total_bal=totalBalance)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("symbol cannot be blank", 400)

        elif not request.form.get("shares") or 0 > float(request.form.get("shares")):
            return apology("shares cannot be empty/negative", 400)

        symbol = lookup(request.form.get("symbol"))

        if not symbol:
            return apology("symbol not found", 400)

        price = symbol["price"]
        balance = db.execute(
            "SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]

        new_balance = balance - (price * float(request.form.get("shares")))

        if new_balance < 0:
            return apology("not enough money")

        else:
            db.execute("UPDATE users SET cash = ? WHERE id = ?",
                       new_balance, session["user_id"])
            db.execute("INSERT INTO transactions (symbol, quantity, price, u_id) VALUES(?, ?, ?, ?)",
                       request.form.get("symbol"), float(request.form.get("shares")), price, session["user_id"])
            return redirect("/")

    return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    portfolio = db.execute(
        "SELECT t_id, symbol, quantity, price, u_id FROM transactions WHERE u_id=? ORDER BY t_id DESC", session["user_id"])

    return render_template("history.html", port=portfolio)


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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    submitted = False
    if request.method == "POST":
        submitted = True
        result = lookup(request.form.get("symbol"))
        if not result:
            return apology("symbol not found")
        time = get_time()
        return render_template("quote.html", results=result, currTime=time, submitted=submitted)
    return render_template("quote.html", results=None)


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


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    portfolio = db.execute(
        "SELECT symbol, SUM(quantity) FROM transactions WHERE u_id=? GROUP BY symbol", session["user_id"])

    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("please select what to sell", 403)

        if not request.form.get("shares") or 0 > int(request.form.get("shares")):
            return apology("shares cannot be empty or negative", 403)

        # check if it's a number
        if not request.form.get("shares").isdigit():
            return apology("shares must be a number", 403)

        if int(request.form.get("shares")) > portfolio[int(request.form.get("symbol"))]["SUM(quantity)"]:
            return apology("not enough shares owned", 403)

        balance = db.execute(
            "SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]
        symbol = portfolio[int(request.form.get("symbol"))]["symbol"]
        price = lookup(symbol)["price"]
        new_balance = balance + (int(request.form.get("shares"))*price)
        db.execute("UPDATE users SET cash = ? WHERE id = ?",
                   new_balance, session["user_id"])
        db.execute("INSERT INTO transactions (symbol, quantity, price, u_id) VALUES(?, ?, ?, ?)",
                   symbol, -int(request.form.get("shares")), price, session["user_id"])

        return redirect("/")

    return render_template("sell.html", port=portfolio)


@app.route("/delete")
@login_required
def delete():
    i = session["user_id"]
    session.clear()
    db.execute("DELETE FROM users WHERE id=?", i)

    return redirect("/login")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)
