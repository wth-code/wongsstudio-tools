# modules
from flask import Flask, redirect, render_template, request, flash, url_for
import smtplib
from flask_table import Table, Col
from firebase import firebase
from datetime import datetime
import pytz
import multiprocessing

# my file
import emailSend
import bmi_calculator
import covid_virus
import randnum
import btt
import ytthumb
from weather import get_weather
from stock import get_stock

app = Flask(__name__)
app.secret_key = "super secret key"
country_time_zone = pytz.timezone('Asia/Hong_Kong')
country_time = datetime.now(country_time_zone)
firebase = firebase.FirebaseApplication("https://stock-3fba6-default-rtdb.firebaseio.com/", None)


@app.route("/")
def home():
    return render_template("index.html")


# =================   EMAIL SENDER  ====================

@app.route("/send", methods=["GET", "POST"])
def send():
    return emailSend.send()


# ===============   END OF EMAIL SENDER  ===================


# =======================   BMI  ===========================

@app.route("/bmi", methods=["GET", "POST"])
def bmi():
    return bmi_calculator.calculate()


# ====================   END BMI   ============================


# ===================    COVID    ==============================

@app.route("/covid", methods=["GET", "POST"])
def covid():
    return covid_virus.grab_info()


# ======================   END COVID   ===========================


# ======================   RANDOM NUM   ==========================

@app.route("/rand_num", methods=["GET", "POST"])
def rad_num():
    return randnum.rand()


# ===================    END RANDOM NUM   =======================


# =======================   YT Thumb   =========================

@app.route("/ytthumb", methods=["GET", "POST"])
def yt():
    return ytthumb.get_thumb()


# ====================   END YT Thumb  =========================


# ==================     BINARY TRANSLATE   =======================

@app.route("/text_to_binary", methods=["GET", "POST"])
def binary_to_text():
    return btt.binary_to_text()


@app.route("/binary_to_text", methods=["GET", "POST"])
def text_to_binary():
    return btt.text_to_binary()


# ====================   END BINARY TRANSLATE   ====================


# ====================     MORE TOOLS   ==========================

@app.route("/more")
def more():
    return render_template("more.html")


# ====================   END MORE TOOLS   ====================


# ====================  Privacy Policy   ====================

@app.route("/p")
def p():
    return render_template("p.html")


# ====================  END Privacy Policy   ====================

# =========================== STOCK ==============================

@app.route("/stock")
def stock():
    return get_items(
        get_date_now()) + "other dates please go to link https://wth-code-emailsender-web.zeet.app/stock/(date) date format is dd-mm-yy"


@app.route("/stock/<date>")
def stock_date(date):
    return get_items(date)


# ========================= END STOCK =============================

class ItemTable(Table):
    name = Col('Time')
    description = Col('Price')


def get_date_now():
    country_time = datetime.now(country_time_zone)
    return country_time.strftime("%d-%m-%y")


def get_items(date):
    result = firebase.get(date, "")
    items = []
    for time, price in result.items():
        items.append(dict(name=time, description=price))
    table = ItemTable(items, border="1")
    return table.__html__()


def listToString(s):
    # initialize an empty string
    str1 = " "

    # return string
    return str1.join(s)


s = smtplib.SMTP('smtp.gmail.com', 587)


if __name__ == "__main__":
    multiprocessing.Process(target=get_weather.doit).start()
    multiprocessing.Process(target=get_stock.get_now).start()
    app.debug = True
    app.run(host="0.0.0.0", port=5000)
