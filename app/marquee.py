import requests
import json
import os

auth_data = {
    "grant_type": "client_credentials",
    "client_id": os.getenv("MARQUEE_CLIENT_ID"),
    "client_secret": os.getenv("MARQUEE_CLIENT_SECRET"),
    "scope": "read_product_data"
}


def get_marquee_data(ticker):
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
        "startDate": "2017-01-15",
        "endDate": "2018-01-15"
    }

    request = session.post(url=request_url, json=request_query)
    results = json.loads(request.text)

    return results
