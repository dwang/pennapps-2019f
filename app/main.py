from flask import Flask
app = Flask(__name__)

from dotenv import load_dotenv
load_dotenv()

from marquee import get_marquee_data

@app.route("/")
def hello_world():
    return "Hello World from Flask"

@app.route("/api/marquee/<ticker>")
def marquee_data(ticker):
    return get_marquee_data(ticker)

if __name__ == "__main__":
    app.run(debug=True, port=8000)
