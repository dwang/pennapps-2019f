import marquee
import alphavantage
import requests
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if request.method == "POST":
        if not request.form.get("ticker"):
            return redirect(url_for("home"))

        ticker = request.form.get("ticker").split("-")[0].strip()
        data = marquee.query_dataset(ticker)
        integrated_factor = []
        growth = []
        financial_returns = []
        multiple = []

        for i in range(120):
            growth.append(data["data"][i * int(len(data["data"]) / 120) - 1]["growthScore"])
            financial_returns.append(data["data"][i * int(len(data["data"]) / 120) - 1]["financialReturnsScore"])
            multiple.append(data["data"][i * int(len(data["data"]) / 120) - 1]["multipleScore"])
            integrated_factor.append(data["data"][i * int(len(data["data"]) / 120) - 1]["integratedScore"])

        return render_template("dashboard.html", ticker=request.form.get("ticker"), integrated_factor=integrated_factor, growth=growth, financial_returns=financial_returns, multiple=multiple)

    return redirect(url_for("home"))


@app.route("/api/automl/query/<sentiment_score>")
def automl_query(sentiment_score):
    data = { "payload": { "row": { "values": [ "0.298", "31.9346", "10/9/2014", "0.74", "0.204" ], "columnSpecIds": [ "6570527555961487360", "8876370565175181312", "3111763042140946432", "7723449060568334336", "1958841537534099456" ] } } }
    r = requests.post("https://automl.googleapis.com/v1beta1/projects/193759269805/locations/us-central1/models/TBL5254566069141504000:predict", data=data, headers={"Authorization": "Bearer AIzaSyB-q9QT3T2wraShhju7tKa1UQetvAsyZVs"})
    return r.text


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
