import time

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

# custom filter
app.jinja_env.filters["usd"] = usd

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

@app.route("/")
@login_required
def index():
    curr_username = db.execute("SELECT username FROM users WHERE id = :session_id", session_id=session["user_id"])
    curr_stocks = db.execute("SELECT * FROM userstocks WHERE username = :username", username=curr_username[0]["username"])

    curr_cash = db.execute("SELECT cash FROM users WHERE username = :username", username=curr_username[0]["username"])
    user_cash = float(curr_cash[0]["cash"])

    user_total = 0

    for total in curr_stocks:
        stock_data = lookup(total["share_symbol"])
        curr_price = stock_data["price"]
        user_total += float(total["share_count"]) * float(curr_price)
        db.execute("UPDATE userstocks SET price = :price WHERE share_symbol = :symbol", price = usd(float(curr_price)), symbol=total["share_symbol"])


    return render_template("index.html", stocks=curr_stocks, cash=usd(user_cash), total=usd(user_total + user_cash))

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock."""
    if(request.method == "POST"):
        if not request.form.get("symbol"):
            return apology("must provide symbol")
        elif not request.form.get("shares"):
            return apology("must provide shares")
        elif float(request.form.get("shares")) < 0:
            return apology("shares must be positive")

        # create variables to safe values
        curr_username = db.execute("SELECT username FROM users WHERE id = :session_id", session_id=session["user_id"])
        curr_shares = float(request.form.get("shares"))
        curr_stock = lookup(request.form.get("symbol"))
        curr_cash = db.execute("SELECT cash FROM users WHERE id = :session_id", session_id=session["user_id"])

        # insert into userstocks if not existing, else update userstocks
        result = db.execute("SELECT share_symbol FROM userstocks WHERE username = :username AND share_symbol = :share_symbol", \
            username=curr_username[0]["username"], share_symbol=curr_stock["symbol"])

        if not result:
            # check for enough money
            if float(curr_cash[0]["cash"]) < curr_stock["price"] * float(curr_shares):
                return apology("not enough money")

            db.execute("INSERT INTO userstocks (username, share_count, share_symbol, \
                price, total, name) VALUES (:username, :share_count, :share_symbol, :price, :total, :name)", \
                username=curr_username[0]["username"], share_count=curr_shares, share_symbol=curr_stock["symbol"], \
                price=usd(curr_stock["price"]), total=usd(curr_stock["price"] * curr_shares), name=curr_stock["name"])
            # subtract stock prizes from current cash
            db.execute("UPDATE users SET cash = cash - :costs WHERE id = :session_id", \
            costs=curr_stock["price"] * curr_shares, session_id=session["user_id"])

            # insert transaction into transactions table
            db.execute("INSERT INTO transactions (username, price, symbol, shares, transaction) VALUES (:username, :price, :symbol, :shares, 'Bought')", \
            username=curr_username[0]["username"], price=curr_stock["price"] * curr_shares, \
            symbol=curr_stock["symbol"], shares=curr_shares)

        else:
            # check for enough money
            if float(curr_cash[0]["cash"]) < curr_stock["price"] * float(curr_shares):
                return apology("not enough money")

        # get total shares number
        user_shares = db.execute("SELECT share_count FROM userstocks WHERE username = :username AND share_symbol = :share_symbol", \
        username=curr_username[0]["username"], share_symbol=curr_stock["symbol"])

        db.execute("UPDATE userstocks SET share_count = share_count + :shares, price = :price, \
        total = :total, name = :name WHERE username = :username AND share_symbol = :share_symbol", \
        shares=curr_shares, username=curr_username[0]["username"], share_symbol=curr_stock["symbol"], \
        price=usd(curr_stock["price"]), name=curr_stock["name"], total=usd((curr_shares * float(curr_stock["price"])) + (float(user_shares[0]["share_count"]) * float(curr_stock["price"]))))

        # subtract stock prizes from current cash
        db.execute("UPDATE users SET cash = cash - :costs WHERE id = :session_id", \
        costs=curr_stock["price"] * curr_shares, session_id=session["user_id"])

        # insert transaction into transactions table
        db.execute("INSERT INTO transactions (username, price, symbol, shares, kind) VALUES (:username, :price, :symbol, :shares, 'Bought')", \
        username=curr_username[0]["username"], price=curr_stock["price"] * curr_shares, \
        symbol=curr_stock["symbol"], shares=curr_shares)

        return redirect(url_for("index"))

    else:
        return render_template("buy.html")

@app.route("/history")
@login_required
def history():
    """Show history of transactions."""
    return apology("TODO")

@app.route("/login", methods=["GET", "POST"])
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

@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        # ensure stock symbol was submitted
        if not request.form.get("quote"):
            return apology("must provide stock symbol")

        stock = lookup(request.form.get("symbol"))

        if stock == None:
            return apology("could not retrieve stock information")

        return render_template("quoted.html", stock=stock)

    else:
        return render_template("quote.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""

    session.clear()

    if request.method == "POST":
        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        elif not request.form.get("retype-password"):
            return apology("must retype password")
        elif pwd_context.encrypt(request.form.get("password")) != pwd_context.encrypt(request.form.get("retype-password")):
            return apology("passwords do not match")

        result = db.execute("INSERT INTO users (username,hash) VALUES (:username, :hashed)", \
            username=request.form.get("username"), \
            hashed=pwd_context.encrypt(request.form.get("password")))

        if not result:
            return apology("username is already existing")

        return redirect(url_for("login"))
    else:
        return render_template("register.html")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock."""

    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("must provide symbol")
        elif not request.form.get("shares"):
            return apology("must provide shares")
        elif float(request.form.get("shares")) < 0:
            return apology("shares must be positive")

        curr_username = db.execute("SELECT username FROM users WHERE id = :session_id", session_id=session["user_id"])
        user_shares = db.execute("SELECT share_count FROM userstocks WHERE username = :username", username=curr_username[0]["username"])
        user_cash = db.execute("SELECT cash FROM users WHERE username = :username", username = curr_username[0]["username"])

        if not user_shares:
            return apology("you don't have shares of this stock")
        elif float(user_shares[0]["share_count"]) < float(request.form.get("shares")):
            return apology("you don't have that many shares of this stock")
        elif float(user_shares[0]["share_count"]) - float(request.form.get("shares")) == 0:
            curr_stock = lookup(request.form.get("symbol"))
            curr_shares = float(request.form.get("shares"))
            curr_id = db.execute("SELECT rowid FROM userstocks WHERE username = :username AND share_symbol = :symbol", \
                username=curr_username[0]["username"], symbol=curr_stock["symbol"])
            print (curr_id)
            db.execute("UPDATE users SET cash = cash + :cash", cash=float(curr_stock["price"]) * curr_shares)
            db.execute("DELETE FROM userstocks WHERE rowid = :rowid", rowid=float(curr_id[0]["id"]))
        else:
            curr_stock = lookup(request.form.get("symbol"))
            curr_shares = float(request.form.get("shares"))

            foo_shares = db.execute("SELECT share_count FROM userstocks WHERE username = :username AND share_symbol = :symbol", \
                username=curr_username[0]["username"], symbol=curr_stock["symbol"])
            user_shares = float(foo_shares[0]["share_count"])
            print(user_shares)
            user_shares -= curr_shares

            db.execute("UPDATE userstocks SET share_count = :shares, total = :total WHERE share_symbol = :symbol AND username = :username", \
                shares=user_shares, total=float(curr_stock["price"]) * user_shares, \
                symbol=curr_stock["symbol"], username=curr_username[0]["username"])

            db.execute("UPDATE users SET cash = cash + :cash WHERE username = :username", \
                cash=float(curr_stock["price"]) * curr_shares, username=curr_username[0]["username"])



        return redirect(url_for("index"))
    else:
        return render_template("sell.html")
