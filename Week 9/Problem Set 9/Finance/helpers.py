import os
import requests
import urllib.parse
import datetime

from flask import redirect, render_template, request, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


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


def lookup(symbol):
    """Look up quote for symbol."""

    # Contact API
    try:
        api_key = os.environ.get("API_KEY")
        url = f"https://api.iex.cloud/v1/data/core/quote/{urllib.parse.quote_plus(symbol)}?token={api_key}"
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        quote = response.json()[0]
        return {
            "name": quote["companyName"],
            "price": float(quote["latestPrice"]),
            "symbol": quote["symbol"],
            "avgTotalVolume": quote["avgTotalVolume"],
            "calculationPrice": quote["calculationPrice"],
            "change": quote["change"],
            "changePercent": quote["changePercent"],
            "close": quote["close"],
            "closeTime": quote["closeTime"],
            "currency": quote["currency"],
            "delayedPrice": quote["delayedPrice"],
            "delayedPriceTime": quote["delayedPriceTime"],
            "extendedChange": quote["extendedChange"],
            "extendedChangePercent": quote["extendedChangePercent"],
            "extendedPrice": quote["extendedPrice"],
            "extendedPriceTime": quote["extendedPriceTime"],
            "high": quote["high"],
            "highSource": quote["highSource"],
            "highTime": quote["highTime"],
            "iexAskPrice": quote["iexAskPrice"],
            "iexAskSize": quote["iexAskSize"],
            "iexBidPrice": quote["iexBidPrice"],
            "iexBidSize": quote["iexBidSize"],
            "iexClose": quote["iexClose"],
            "iexCloseTime": quote["iexCloseTime"],
            "iexLastUpdated": quote["iexLastUpdated"],
            "iexMarketPercent": quote["iexMarketPercent"],
            "iexOpen": quote["iexOpen"],
            "iexOpenTime": quote["iexOpenTime"],
            "iexRealtimePrice": quote["iexRealtimePrice"],
            "iexRealtimeSize": quote["iexRealtimeSize"],
            "iexVolume": quote["iexVolume"],
            "lastTradeTime": quote["lastTradeTime"],
            "latestPrice": quote["latestPrice"],
            "latestSource": quote["latestSource"],
            "latestTime": quote["latestTime"],
            "latestUpdate": quote["latestUpdate"],
            "latestVolume": quote["latestVolume"],
            "low": quote["low"],
            "lowSource": quote["lowSource"],
            "lowTime": quote["lowTime"],
            "marketCap": quote["marketCap"],
            "oddLotDelayedPrice": quote["oddLotDelayedPrice"],
            "oddLotDelayedPriceTime": quote["oddLotDelayedPriceTime"],
            "open": quote["open"],
            "openTime": quote["openTime"],
            "openSource": quote["openSource"],
            "peRatio": quote["peRatio"],
            "previousClose": quote["previousClose"],
            "previousVolume": quote["previousVolume"],
            "primaryExchange": quote["primaryExchange"],
            "volume": quote["volume"],
            "week52High": quote["week52High"],
            "week52Low": quote["week52Low"],
            "ytdChange": quote["ytdChange"],
            "isUSMarketOpen": quote["isUSMarketOpen"]
        }
    except (KeyError, TypeError, ValueError):
        return None


def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"


def get_time():
    """Get current time"""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def format_time(time):
    """Format time"""
    timestamp = time  # example value of latestUpdate
    # time zone you want to display the time in
    dt = datetime.datetime.fromtimestamp(timestamp / 1000)
    # prints the time in 12-hour format with AM/PM and the time zone abbreviation
    return dt.strftime("%I:%M %p %Z").lstrip("0")
   # return datetime.datetime.fromtimestamp(time / 1000).strftime("%B %d, %I:%M %p")


def format_money(value):
    if value >= 1000000000:
        return f"{value / 1000000000:.2f}B"
    elif value >= 1000000:
        return f"{value / 1000000:.2f}M"
    else:
        return value
