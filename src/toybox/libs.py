from toybox.src.toybox.decorator import logging
import requests
import datetime
import time
import numpy as np

@logging
def call_restapi(type="GET", url="", headers={}) -> dict:
    return requests.request(type, url, headers=headers).json()


def get_data(client=None, market="KRW-BTC", type="minutes", from_date=[2021, 1, 1, 0, 0, 0], to_date=""):
    """
    minutes : url = "https://api.upbit.com/v1/candles/minutes/1?market=KRW-BTC&to=2021-11-23%2010%3A00%3A01&count=5"
    url           = 'https://api.upbit.com/v1/candles/minutes/1?market=KRW-BTC&to=2021-11-23%2015$3A26%3A00&count=86'
    url           = "https://api.upbit.com/v1/candles/minutes/1?market=KRW-BTC&to=2021-11-23%2015%3A26%3A00&count=1"
    days : url = "https://api.upbit.com/v1/candles/days?market=KRW-BTC&to=2021-10-10%2000%3A00%3A00&count=2"

    headers = {"Accept": "application/json"}
    response = requests.request("GET", url, headers=headers)
    """
    base_url = "https://api.upbit.com/v1/candles/"
    headers = {"Accept": "application/json"}
    ret = list()

    if type == "minutes":
        type = type + "/1"
        time_delta = datetime.timedelta(minutes=1)
    elif type == "days":
        time_delta = datetime.timedelta(days=1)
    elif type == "weeks":
        time_delta = datetime.timedelta(days=7)
    elif type == "months":
        pass
    
    time_cursor = datetime.datetime(from_date[0], from_date[1], from_date[2], from_date[3], from_date[4], from_date[5],tzinfo=datetime.timezone.utc)
    time_now = datetime.datetime.now(datetime.timezone.utc)

    if time_now < time_cursor:
        raise Exception(f"invalid time, UTC : {time_cursor}")
    while time_cursor < time_now:
        count = 0
        temp_ret = list()

        while time_cursor < time_now and count < 200:
            time_cursor += time_delta
            count += 1
        
        time_str = str(time_cursor).split("+")[0].replace(":", "%3A")
        url = f"{base_url}{type}?market={market}&to={time_str}&count={count}"
        
        while not check_can_call(client=client):
            time.sleep(1)

        response = call_restapi(type="GET", url=url, headers=headers)
        
        for i in response:
            temp_ret.append(i)
        temp_ret.reverse()
        for i in temp_ret:
            ret.append(i)
    
    return ret
    

def check_can_call(client=None):
    resp = client.APIKey.APIKey_info()
    if "error" in resp["result"]:
        return False
    return True


def get_std(data=list()) -> dict :
    stds = {
        "high_by_open": 0,
        "high_by_close": 0,
        "low_by_open": 0,
        "low_by_close": 0,
        "Hclose_by_open": 0,
        "Lclose_by_open": 0,
        "Htail_by_close": 0,
        "Ltail_by_close": 0,
    }
    arrs = {
        "high_by_open": np.array([]),
        "high_by_close": np.array([]),
        "low_by_open": np.array([]),
        "low_by_close": np.array([]),
        "Hclose_by_open": np.array([]),
        "Lclose_by_open": np.array([]),
        "Htail_by_close": np.array([]),
        "Ltail_by_close": np.array([]),
    }
    for d in data:
        open = float(d.get("opening_price", ""))
        close = float(d.get("trade_price", ""))
        high = float(d.get("high_price", ""))
        low = float(d.get("low_price", ""))
        if close >= open:
            arrs["high_by_open"] = np.append(arrs["high_by_open"], np.array([(high - open) / open]))
            arrs["high_by_close"] = np.append(arrs["high_by_close"], np.array([(high - close) / close]))
            arrs["Hclose_by_open"] = np.append(arrs["Hclose_by_open"], np.array([(close - open) / open]))
            arrs["Htail_by_close"] = np.append(arrs["Htail_by_close"], np.array([((high - open) / open) - ((close - open) / open)]))
        else:
            arrs["low_by_open"] = np.append(arrs["low_by_open"], np.array([(low - open) / open]))
            arrs["low_by_close"] = np.append(arrs["low_by_close"], np.array([(low - close) / close]))
            arrs["Lclose_by_open"] = np.append(arrs["Lclose_by_open"], np.array([(close - open) / open]))
            arrs["Ltail_by_close"] = np.append(arrs["Ltail_by_close"], np.array([((low - open) / open) - ((close - open) / open)]))
    
    stds["high_by_open"] = np.std(arrs["high_by_open"])
    stds["high_by_close"] = np.std(arrs["high_by_close"])
    stds["low_by_open"] = np.std(arrs["low_by_open"])
    stds["low_by_close"] = np.std(arrs["low_by_close"])
    stds["Hclose_by_open"] = np.std(arrs["Hclose_by_open"])
    stds["Lclose_by_open"] = np.std(arrs["Lclose_by_open"])
    stds["Htail_by_close"] = np.std(arrs["Htail_by_close"])
    stds["Ltail_by_close"] = np.std(arrs["Ltail_by_close"])
    
    return stds

if __name__ == "__main__":
    print("Hello")