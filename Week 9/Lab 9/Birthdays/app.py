import os

# Import the Flask Framework
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")


@app.route("/", methods=["GET", "POST"])
def index():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Add the user's entry into the database
        name = request.form.get("name")
        month = request.form.get("month")
        day = request.form.get("day")
        db.execute(
            "INSERT INTO birthdays (name, month, day) VALUES(?, ?, ?)", name, month, day)

        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        # Display the entries in the database on index.html
        notes = db.execute("SELECT * FROM birthdays")
        return render_template("index.html", notes=notes)
