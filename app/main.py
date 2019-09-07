import marquee
from flask import Flask
app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello World from Flask"


@app.route("/api/marquee/query/<ticker>")
def query_dataset(ticker):
    return marquee.query_dataset(ticker)

@app.route("/api/marquee/asset/<ticker>")
def get_asset(ticker):
    return marquee.get_asset(ticker)

if __name__ == "__main__":
    app.run(debug=True, port=8000)
