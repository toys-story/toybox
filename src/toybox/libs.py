from upbit.client import Upbit
import requests
import datetime
import json

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
    while time_cursor < time_now:
        count = 0
        
        while time_cursor < time_now and count < 200:
            time_cursor += time_delta
            count += 1
        
        time_str = str(time_cursor).split("+")[0].replace(":", "%3A")
        url = f"{base_url}{type}?market={market}&to={time_str}&count={count}"    
        response = requests.request("GET", url, headers=headers).json()
        print("call rest api !")
        
        for i in response:
            ret.append(i)
    
    return ret
    
    

if __name__ == "__main__":
    # time_now = datetime.datetime.now(datetime.timezone.utc)
    time_now = datetime.datetime(2021, 1, 1, 0, 0, 0)
    str_time = str(time_now).split("+")[0]
    t = str_time.replace(":", "%3A")
    delta = datetime.timedelta(minutes=1)
    date = datetime.datetime(2021, 1, 1, 0, 0, 0)
    today = datetime.datetime.today()
    
    for i in range(200):
        date += delta
        print(date)
    print(today - date)
    print((today-date)/delta)