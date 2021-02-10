from firebase import firebase
import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
import pytz

country_time_zone = pytz.timezone('Asia/Hong_Kong')
firebase = firebase.FirebaseApplication("https://stock-3fba6-default-rtdb.firebaseio.com/", None)
headers_g = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36"
}

def get_date_now():
    country_time = datetime.now(country_time_zone)
    return country_time.strftime("%d-%m-%y")

def get_time_now():
    country_time = datetime.now(country_time_zone)
    return country_time.strftime("%d-%m-%y %H:%M:%S")


def get_time():
    country_time = datetime.now(country_time_zone)
    return country_time.strftime("%H:%M:%S")


def get_stock():
    url = "http://www.aastocks.com/en/stocks/market/index/hk-index-con.aspx"
    sess = requests.session()
    req = sess.get(url, headers=headers_g)
    soup = BeautifulSoup(req.text, features="html.parser")
    result = soup.find_all("div", class_="hkidx-last txt_r")[0].text
    return result


def get_now():
    while True:
        if int(get_time().split(":")[0]) < 16 and int(get_time().split(":")[0]) > 9:
            firebase.put(get_date_now(), get_time_now(), get_stock())
            time.sleep(60)
        elif int(get_time().split(":")[0]) == 16 and int(get_time().split(":")[1]) < 30:
            firebase.put(get_date_now(), get_time_now(), get_stock())
            time.sleep(60)