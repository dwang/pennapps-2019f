import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

auth_data = {
    "grant_type": "client_credentials",
    "client_id": os.getenv("MARQUEE_CLIENT_ID"),
    "client_secret": os.getenv("MARQUEE_CLIENT_SECRET"),
    "scope": "read_product_data"
}


def query_dataset(ticker):
    session = requests.Session()

    auth_request = session.post(
        "https://idfs.gs.com/as/token.oauth2", data=auth_data)
    access_token_dict = json.loads(auth_request.text)
    access_token = access_token_dict["access_token"]

    session.headers.update({"Authorization": "Bearer " + access_token})

    request_url = "https://api.marquee.gs.com/v1/data/USCANFPP_MINI/query"

    request_query = {
        "where": {
            "ticker": ticker
        },
        "startDate": "2012-07-01"
    }

    request = session.post(
        url="https://api.marquee.gs.com/v1/data/USCANFPP_MINI/query", json=request_query)
    results = json.loads(request.text)

    return results


def get_asset(ticker):
    session = requests.Session()

    auth_request = session.post(
        "https://idfs.gs.com/as/token.oauth2", data=auth_data)
    access_token_dict = json.loads(auth_request.text)
    access_token = access_token_dict["access_token"]

    session.headers.update({"Authorization": "Bearer " + access_token})

    request_url = "https://api.marquee.gs.com/v1/assets"

    request = session.get(url=request_url, params={
                          "ticker": ticker, "assetClassificationsIsPrimary": "true"})
    results = json.loads(request.text)

    return results


def get_marquee_tickers():
    session = requests.Session()

    auth_request = session.post(
        "https://idfs.gs.com/as/token.oauth2", data=auth_data)
    access_token_dict = json.loads(auth_request.text)
    access_token = access_token_dict["access_token"]

    session.headers.update({"Authorization": "Bearer " + access_token})

    coverage = session.get(
        url="https://api.marquee.gs.com/v1/data/USCANFPP_MINI/coverage?limit=200")
    coverage_data = json.loads(coverage.text)

    reference_query = {
        "where": {
            "gsid": [point["gsid"] for point in coverage_data["results"]]
        },
        "fields": ["gsid", "ticker", "name"],
        "limit": 200
    }

    reference = session.post(
        url="https://api.marquee.gs.com/v1/assets/data/query", json=reference_query)
    reference_data = json.loads(reference.text)
    companies_set = {(result["ticker"], result["name"])
                     for result in reference_data["results"]}

    with open("static/companies.json", "w") as out:
        json.dump(list(companies_set), out)


if __name__ == "__main__":
    get_marquee_tickers()
