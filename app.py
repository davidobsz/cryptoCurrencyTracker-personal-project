import time
from flask import Flask, jsonify, render_template
import requests
import mplfinance as mpf
from datetime import datetime
import pandas as pd
import base64


def btc_klines_one_minute_30_min():
    while True:
        key = "https://api.binance.us/api/v3/klines?symbol=BTCUSDT&interval=1m&limit=31"
        data = requests.get(key)
        data = data.json()
        #print(data)
        # kline open time, open price, high price, low price, close price, volume, kline close time, quote asset volume, number of trades
        return data


def btc_klines_one_hour_1_week():
    while True:
        key = "https://api.binance.us/api/v3/klines?symbol=BTCUSDT&interval=4h&limit=42"
        data = requests.get(key)
        data = data.json()
        #print(data)
        # kline open time, open price, high price, low price, close price, volume, kline close time, quote asset volume, number of trades
        return data

def eth_klines_one_minute_30_min():
    while True:
        key = "https://api.binance.us/api/v3/klines?symbol=ETHUSDT&interval=1m&limit=31"
        data = requests.get(key)
        data = data.json()
        #print(data)
        # kline open time, open price, high price, low price, close price, volume, kline close time, quote asset volume, number of trades
        return data


def eth_klines_one_hour_1_week():
    while True:
        key = "https://api.binance.us/api/v3/klines?symbol=ETHUSDT&interval=4h&limit=42"
        data = requests.get(key)
        data = data.json()
        #print(data)
        # kline open time, open price, high price, low price, close price, volume, kline close time, quote asset volume, number of trades
        return data


app = Flask(__name__)

def btc_price():
    while True:
        key = "https://api.binance.us/api/v3/ticker/price?symbol=BTCUSDT"
        data = requests.get(key)
        data = data.json()
        return f"{data['symbol']} price is ${round(float((data['price'])), 3)}"

def eth_price():
    while True:
        key = "https://api.binance.us/api/v3/ticker/price?symbol=ETHUSDT"
        data = requests.get(key)
        data = data.json()
        return f"{data['symbol']} price is ${round(float((data['price'])), 3)}"



@app.route('/home', methods=['GET'])
def home():
    return render_template("home.html")

@app.route('/', methods=['GET'])
def hello_world():

    # last 30 min
    # -----------------------------------------------------------------------
    btc_last_30_min = pd.DataFrame()
    btc_last_30_min.index = pd.to_datetime(btc_last_30_min.index)

    btc_price()
    btc_klines_one_minute_30_min()

    for x in btc_klines_one_minute_30_min():
        #print(x[1], x[4], x[2], x[3])
        my_timestamp = x[0]
        my_timestamp = str(my_timestamp)[:-3]
        my_timestamp = int(my_timestamp) + 3600
        my_datetime = datetime.fromtimestamp(my_timestamp)
        #print(my_datetime)

        btc_last_30_min.loc[f"{my_datetime}", "open"] = float(x[1])
        btc_last_30_min.loc[f"{my_datetime}", "close"] = float(x[4])
        btc_last_30_min.loc[f"{my_datetime}", "high"] = float(x[2])
        btc_last_30_min.loc[f"{my_datetime}", "low"] = float(x[3])
        btc_last_30_min.loc[f"{my_datetime}", "volume"] = float(x[5])


    data = btc_price()
    mpf.plot(btc_last_30_min, type="candle",volume=True, savefig="testsave.png", style="yahoo", title="BTC Price", mav=(3, 6, 9))
    with open("testsave.png", "rb") as f:
        contents = f.read()

    # Encode the contents as a Base64 string
    encoded = base64.b64encode(contents).decode("utf-8")

    # Construct the data URL
    url = "data:image/png;base64," + encoded
    # -----------------------------------------------------------------------

    # last 1 week
    # -----------------------------------------------------------------------
    btc_last_1_week = pd.DataFrame()
    btc_last_1_week.index = pd.to_datetime(btc_last_1_week.index)

    btc_price()
    btc_klines_one_hour_1_week()

    for x in btc_klines_one_hour_1_week():
        # print(x[1], x[4], x[2], x[3])
        my_timestamp = x[0]
        my_timestamp = str(my_timestamp)[:-3]
        my_timestamp = int(my_timestamp) + 3600
        my_datetime = datetime.fromtimestamp(my_timestamp)
        # print(my_datetime)

        btc_last_1_week.loc[f"{my_datetime}", "open"] = float(x[1])
        btc_last_1_week.loc[f"{my_datetime}", "close"] = float(x[4])
        btc_last_1_week.loc[f"{my_datetime}", "high"] = float(x[2])
        btc_last_1_week.loc[f"{my_datetime}", "low"] = float(x[3])
        btc_last_1_week.loc[f"{my_datetime}", "volume"] = float(x[5])

    # data = btc_price()

    mpf.plot(btc_last_1_week, type="candle", volume=True, savefig="testsave.png", style="yahoo", title="BTC Price",
             mav=(3, 6, 9))
    with open("testsave.png", "rb") as f:
        contents = f.read()

    # Encode the contents as a Base64 string
    encoded2 = base64.b64encode(contents).decode("utf-8")

    # Construct the data URL
    url2 = "data:image/png;base64," + encoded2
    # -----------------------------------------------------------------------

    return render_template("index.html", data=data, img_30_min=url,img_1_week=url2)


@app.route('/eth', methods=['GET'])
def eth():

    # last 30 min
    # -----------------------------------------------------------------------
    eth_last_30_min = pd.DataFrame()
    eth_last_30_min.index = pd.to_datetime(eth_last_30_min.index)

    eth_price()
    eth_klines_one_minute_30_min()

    for x in eth_klines_one_minute_30_min():
        #print(x[1], x[4], x[2], x[3])
        my_timestamp = x[0]
        my_timestamp = str(my_timestamp)[:-3]
        my_timestamp = int(my_timestamp) + 3600
        my_datetime = datetime.fromtimestamp(my_timestamp)
        #print(my_datetime)

        eth_last_30_min.loc[f"{my_datetime}", "open"] = float(x[1])
        eth_last_30_min.loc[f"{my_datetime}", "close"] = float(x[4])
        eth_last_30_min.loc[f"{my_datetime}", "high"] = float(x[2])
        eth_last_30_min.loc[f"{my_datetime}", "low"] = float(x[3])
        eth_last_30_min.loc[f"{my_datetime}", "volume"] = float(x[5])


    data = eth_price()
    mpf.plot(eth_last_30_min, type="candle",volume=True, savefig="testsave1.png", style="yahoo", title="ETH Price last 30 min", mav=(3, 6, 9))
    with open("testsave1.png", "rb") as f:
        contents = f.read()

    # Encode the contents as a Base64 string
    encoded = base64.b64encode(contents).decode("utf-8")

    # Construct the data URL
    url = "data:image/png;base64," + encoded
    # -----------------------------------------------------------------------

    # last 1 week
    # -----------------------------------------------------------------------
    eth_last_1_week = pd.DataFrame()
    eth_last_1_week.index = pd.to_datetime(eth_last_1_week.index)

    eth_price()
    eth_klines_one_hour_1_week()

    for x in eth_klines_one_hour_1_week():
        # print(x[1], x[4], x[2], x[3])
        my_timestamp = x[0]
        my_timestamp = str(my_timestamp)[:-3]
        my_timestamp = int(my_timestamp) + 3600
        my_datetime = datetime.fromtimestamp(my_timestamp)
        # print(my_datetime)

        eth_last_1_week.loc[f"{my_datetime}", "open"] = float(x[1])
        eth_last_1_week.loc[f"{my_datetime}", "close"] = float(x[4])
        eth_last_1_week.loc[f"{my_datetime}", "high"] = float(x[2])
        eth_last_1_week.loc[f"{my_datetime}", "low"] = float(x[3])
        eth_last_1_week.loc[f"{my_datetime}", "volume"] = float(x[5])

    # data = btc_price()

    mpf.plot(eth_last_1_week, type="candle", volume=True, savefig="testsave1.png", style="yahoo", title="ETH Price last 1 week",
             mav=(3, 6, 9))
    with open("testsave1.png", "rb") as f:
        contents = f.read()

    # Encode the contents as a Base64 string
    encoded2 = base64.b64encode(contents).decode("utf-8")

    # Construct the data URL
    url2 = "data:image/png;base64," + encoded2
    # -----------------------------------------------------------------------

    return render_template("eth.html", data=data, img_30_min=url,img_1_week=url2)



if __name__ == '__main__':
    app.run(debug=True)
