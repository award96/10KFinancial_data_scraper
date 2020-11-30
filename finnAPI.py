import requests
import json
import time

"""
    handle api requests
"""

API_KEY_PATH = "api.txt"


def get_api_key():
    try:
        with open(API_KEY_PATH, 'r') as file:
            api_key_raw = file.readline()
            if "\n" in api_key_raw:
                api_key = api_key_raw.replace("\n", "")
            else:
                api_key = api_key_raw
            return api_key
    except FileNotFoundError as e:
        print(e)
        print("Please include a file named api.txt with your api key in the same folder as this program")
        exit()


API_KEY = get_api_key()


def handle_response(response, callback_function, symbol):

    # catch response 429 (api limit reached) but not other json decoding errors
    try:
        json_resp = response.json()
    except json.decoder.JSONDecodeError as e:
        if (response.status_code != 429):
            raise json.decoder.JSONDecodeError(f"\n\nJSONDecodeError\nresponse status: {response.status_code}\nThis usually means either a bad API key or internet connection issues\n", e.doc, e.pos)
        seconds = 60
        print(f"API rate limit exceeded. Pausing {seconds/60} minute(s)")
        time.sleep(seconds)
        json_resp = callback_function(symbol)
    return json_resp


def get_tenK_json(symbol):
    r = requests.get(
        f'https://finnhub.io/api/v1/stock/financials-reported?symbol={symbol}&token={API_KEY}')
    return handle_response(r, get_tenK_json, symbol)


def get_profile_json(symbol):
    r = requests.get(
        f'https://finnhub.io/api/v1/stock/profile2?symbol={symbol}&token={API_KEY}')
    return handle_response(r, get_profile_json, symbol)

def get_symbol_json(exchange = "US"):
    r = requests.get(
        f'https://finnhub.io/api/v1/stock/symbol?exchange={exchange}')
    return handle_response(r, get_symbol_json, exchange)