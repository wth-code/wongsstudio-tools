from flask import render_template
import requests
from bs4 import BeautifulSoup
import threading


def get_data():
    global death, case, recover
    url = "https://www.worldometers.info/coronavirus/"
    sess = requests.session()
    req = sess.get(url)
    soup = BeautifulSoup(req.text, features="html.parser")
    case = soup.select(".maincounter-number")[0].text
    death = soup.select(".maincounter-number")[1].text
    recover = soup.select(".maincounter-number")[2].text
    return None


def grab_info():
    get_data()
    return render_template("covid.html", case=case, recover=recover, death=death)