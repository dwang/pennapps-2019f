import marquee
import alphavantage
import requests
import os
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
    data = {
        "payload": {
            "row": {
                "values": [
                    sentiment_score
                ],
                "columnSpecIds": [
                    "5129375675202928640"
                ]
            }
        }
    }

    r = requests.post("https://automl.googleapis.com/v1beta1/projects/193759269805/locations/us-central1/models/TBL2464599294125015040:predict", json=data, headers={"Authorization": "Bearer " + os.getenv("GCLOUD_API_KEY")})
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
