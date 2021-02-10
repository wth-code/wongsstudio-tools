from firebase import firebase
import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
import pytz

country_time_zone = pytz.timezone('Asia/Hong_Kong')
firebase = firebase.FirebaseApplication("https://weather-hk-68ce2-default-rtdb.firebaseio.com/", None)

headers_g = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36"
}

def get_time_now():
    country_time = datetime.now(country_time_zone)
    return country_time.strftime("Last update: %d-%m-%y %H:%M:%S")


def icon(icon_link):
    x = icon_link["src"].split("svg/")[1]
    if x == "wt-1.svg":
        return "1.png"
    elif x == "wt-2.svg" or x == "wt-3.svg" or x == "wt-4.svg" or x == "wt-5.svg" or x == "wt-6.svg" or x == "wt-8.svg" or x == "wt-9.svg" or x == "wt-10.svg" or x == "wt-11.svg" or x == "wt-12.svg":
        return "2.png"
    elif x == "wt-7.svg":
        return "3.png"
    elif x == "wt-13.svg":
        return "4.png"
    elif x == "wt-14.svg" or x == "wt-15.svg" or x == "wt-16.svg" or x == "wt-17.svg":
        return "5.png"
    elif x == "wt-18.svg" or x == "wt-19.svg" or x == "wt-20.svg" or x == "wt-34.svg" or x == "wt-33.svg" or x == "wt-32.svg":
        return "6.png"
    elif x == "wt-21.svg" or "wt-22.svg" or "wt-23.svg" or "wt-35.svg":
        return "7.png"
    elif x == "wt-24.svg" or x == "wt-25.svg" or x == "wt-26.svg" or x == "wt-27.svg" or x == "wt-28.svg" or x == "wt-29.svg" or x == "wt-30.svg":
        return "8.png"


def get_degree_now():
    url = "https://www.timeanddate.com/worldclock/hong-kong/hong-kong"
    sess = requests.session()
    req = sess.get(url, headers=headers_g)
    soup = BeautifulSoup(req.text, features="html.parser")
    degree_now = soup.select("#wt-tp")[0].text
    return degree_now


def get_icon_now():
    url = "https://www.timeanddate.com/weather/hong-kong/hong-kong"
    sess = requests.session()
    req = sess.get(url, headers=headers_g)
    soup = BeautifulSoup(req.text, features="html.parser")
    now = soup.find_all("img", class_="mtt")[0]
    return icon(now)


def get_future_icon(x):
    day = [4, 5, 6, 7, 8]
    url = "https://www.timeanddate.com/weather/hong-kong/hong-kong/ext"
    sess = requests.session()
    req = sess.get(url, headers=headers_g)
    soup = BeautifulSoup(req.text, features="html.parser")
    tag = soup.find_all("img")[day[x - 1]]
    return icon(tag)


def get_weather_status():
    url = "https://www.timeanddate.com/worldclock/hong-kong/hong-kong"
    sess = requests.session()
    req = sess.get(url, headers=headers_g)
    soup = BeautifulSoup(req.text, features="html.parser")
    weather_status = soup.select("#wt-3d p")[0].text.split(".")[0]
    return weather_status


def get_humidity():
    url = "https://www.timeanddate.com/weather/hong-kong/hong-kong"
    sess = requests.session()
    req = sess.get(url, headers=headers_g)
    soup = BeautifulSoup(req.text, features="html.parser")
    humidity = soup.select(".bk-focus__info")[0].text.split("Humidity: ")[1].split("Dew Point")[0]
    return humidity


def get_wind_speed():
    url = "https://www.timeanddate.com/weather/hong-kong/hong-kong"
    sess = requests.session()
    req = sess.get(url, headers=headers_g)
    soup = BeautifulSoup(req.text, features="html.parser")
    wind_speed = soup.select(".bk-focus__qlook")[0].text.split("Wind: ")[1].split(" ")[0]
    return (wind_speed)


def get_future_degree(x):
    day = [0, 3, 6, 9, 12]
    url = "https://www.timeanddate.com/weather/hong-kong/hong-kong/ext"
    sess = requests.session()
    req = sess.get(url, headers=headers_g)
    soup = BeautifulSoup(req.text, features="html.parser")
    future = soup.find_all("td", class_="sep")[day[x - 1]].text
    return future


def doit():
    while True:
        last_update = '\"%s\"' % (get_time_now())
        wind_speed = '\"%s\"' % (get_wind_speed())
        degree_now = '\"%s\"' % (get_degree_now())
        weather_status = '\"%s\"' % (get_weather_status())
        humidity = '\"%s\"' % (get_humidity())
        day1_icon = '\"%s\"' % get_future_icon(1)
        day2_icon = '\"%s\"' % get_future_icon(2)
        day3_icon = '\"%s\"' % get_future_icon(3)
        day4_icon = '\"%s\"' % get_future_icon(4)
        day5_icon = '\"%s\"' % get_future_icon(5)
        day1 = '\"%s\"' % (get_future_degree(1))
        day2 = '\"%s\"' % (get_future_degree(2))
        day3 = '\"%s\"' % (get_future_degree(3))
        day4 = '\"%s\"' % (get_future_degree(4))
        day5 = '\"%s\"' % (get_future_degree(5))
        firebase.put("/weather", "degree_now", degree_now)
        firebase.put("/weather", "icon_now", get_icon_now())
        firebase.put("/weather", "weather_status", weather_status)
        firebase.put("/weather", "humidity", humidity)
        firebase.put("/weather", "wind_speed", wind_speed)
        firebase.put("/weather", "day1", day1)
        firebase.put("/weather", "day2", day2)
        firebase.put("/weather", "day3", day3)
        firebase.put("/weather", "day4", day4)
        firebase.put("/weather", "day5", day5)
        firebase.put("/weather", "day1_icon", day1_icon)
        firebase.put("/weather", "day2_icon", day2_icon)
        firebase.put("/weather", "day3_icon", day3_icon)
        firebase.put("/weather", "day4_icon", day4_icon)
        firebase.put("/weather", "day5_icon", day5_icon)
        firebase.put("/time", "last_update", last_update)
        print("weather updated")
        time.sleep(300)