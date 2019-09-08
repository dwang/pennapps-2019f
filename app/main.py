import marquee
import alphavantage
from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if request.method == "POST":
        ticker = request.form.get("ticker")
        data = marquee.query_dataset(ticker)
        return render_template("dashboard.html", ticker=ticker, data=data)

    return redirect(url_for("home"))


@app.route("/api/marquee/query/<ticker>")
def query_dataset(ticker):
    return marquee.query_dataset(ticker)


@app.route("/api/marquee/asset/<ticker>")
def get_asset(ticker):
    return marquee.get_asset(ticker)


@app.route("/api/alphavantage/query/<ticker>/<date>")
def query_prices(ticker, date):
    return alphavantage.query_prices(ticker, date)


if __name__ == "__main__":
    app.run(debug=True, port=8000)
