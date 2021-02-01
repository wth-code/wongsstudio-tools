from flask import Flask, redirect, render_template, request, flash, url_for
import smtplib
import requests
from bs4 import BeautifulSoup
import random
from urllib.parse import urlparse, parse_qs
from flask_table import Table, Col
from firebase import firebase
import time
from datetime import datetime
import pytz

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
    global sender_email, sender_password, sender_title, msg, li_emails
    try:
        s.starttls()
        if request.method == "POST":
            sender_email = request.form["gm"]
            sender_password = request.form["psd"]
            sender_title = request.form["tit"]
            sender_msg = request.form["msg"]
            emails = request.form["st"]
            li_emails = list(emails.split(","))
            msg = f"Subject: {sender_title}\n\n{sender_msg}"
            try:
                s.login(sender_email, sender_password)
                for x in li_emails:
                    if x == li_emails[len(li_emails) - 1]:
                        s.sendmail(sender_email, x, msg)
                        flash("Your email has been sent !")
                    else:
                        s.sendmail(sender_email, x, msg)
            except Exception:
                flash("Error, Try again")
            return render_template("send.html")
        else:
            return render_template("send.html")
    except Exception:
        if request.method == "POST":
            sender_email = request.form["gm"]
            sender_password = request.form["psd"]
            sender_title = request.form["tit"]
            sender_msg = request.form["msg"]
            emails = request.form["st"]
            li_emails = list(emails.split(","))
            msg = f"Subject: {sender_title}\n\n{sender_msg}"
            try:
                s.login(sender_email, sender_password)
                for x in li_emails:
                    if x == li_emails[len(li_emails) - 1]:
                        s.sendmail(sender_email, x, msg)
                        flash(f"Your email has been sent !")
                    else:
                        s.sendmail(sender_email, x, msg)
            except Exception:
                flash("Error, Try again")
            return render_template("send.html")
        else:
            return render_template("send.html")


# ===============   END OF EMAIL SENDER  ===================


# =======================   BMI  ===========================

@app.route("/bmi", methods=["GET", "POST"])
def bmi():
    if request.method == "POST":
        num1 = request.form["num1"]
        num2_get = request.form["num2"]
        num2 = float(num2_get) / 100
        bmi = float(num1) / (float(num2) ** 2)
        flash(f"Your BMI is {bmi}")
    return render_template("bmi.html")


# ====================   END BMI   ============================


# ===================    COVID    ==============================

@app.route("/covid", methods=["GET", "POST"])
def covid():
    url = "https://www.worldometers.info/coronavirus/"
    sess = requests.session()
    req = sess.get(url)
    soup = BeautifulSoup(req.text, features="html.parser")
    case = soup.select(".maincounter-number")[0].text
    death = soup.select(".maincounter-number")[1].text
    recover = soup.select(".maincounter-number")[2].text
    return render_template("covid.html", case=case, recover=recover, death=death)


# ======================   END COVID   ===========================


# ======================   RANDOM NUM   ==========================

@app.route("/rand_num", methods=["GET", "POST"])
def rad_num():
    if request.method == "POST":
        min = request.form["min"]
        max = request.form["max"]
        if min < max:
            num = random.randint(int(min), int(max))
            flash(f"The number is {num}")
        else:
            flash("Min is larger than Max, try again")
        return render_template("rand_num.html")
    else:
        return render_template("rand_num.html")


# ===================    END RANDOM NUM   =======================


# =======================   YT Thumb   =========================

@app.route("/ytthumb", methods=["GET", "POST"])
def ytthumb():
    if request.method == "POST":
        url = request.form["url"]
        if extract_video_id(url):
            id = extract_video_id(url)
            img = f"https://i.ytimg.com/vi/{id}/maxresdefault.jpg"
            flash(img)
            return render_template("yt_thumb.html")
        else:
            flash("Type a YouTube Video URL !")
            return render_template("yt_thumb.html")
    else:
        return render_template("yt_thumb.html")


def extract_video_id(url):
    query = urlparse(url)
    if query.hostname == 'youtu.be': return query.path[1:]
    if query.hostname in {'www.youtube.com', 'youtube.com'}:
        if query.path == '/watch': return parse_qs(query.query)['v'][0]
        if query.path[:7] == '/embed/': return query.path.split('/')[2]
        if query.path[:3] == '/v/': return query.path.split('/')[2]
    # fail
    return False


# ====================   END YT Thumb  =========================


# ==================     BINARY TRANSLATE   =======================

@app.route("/text_to_binary", methods=["GET", "POST"])
def binary_to_text():
    if request.method == "POST":
        txt_input = request.form["uin"]
        bin_done = string_to_binary(txt_input)
        flash(bin_done)
        return render_template("text_to_binary.html", txt_done=txt_input)
    else:
        flash(" ")
        return render_template("text_to_binary.html")


@app.route("/binary_to_text", methods=["GET", "POST"])
def text_to_binary():
    if request.method == "POST":
        bin_input = request.form["uin"]
        txt_done = binary_to_string(bin_input)
        flash(txt_done)
        return render_template("binary_to_text.html", bin_done=bin_input)
    else:
        flash(" ")
        return render_template("binary_to_text.html")


def string_to_binary(string):
    total_binary = ''
    for x in range(0, len(string)):
        binary = ''
        string_ord = ord(string[x: x + 1])
        while string_ord > 0:
            i = string_ord % 2
            string_ord = string_ord // 2
            binary = str(i) + str(binary)
        if len(binary) < 8:
            required_bits = 8 - len(binary)
            for i in range(required_bits):
                binary = '0' + binary
        total_binary += binary + ' '
    return str(total_binary)


def binary_to_string(binary):
    try:
        binary_values = binary.split()
        ascii_string = ""
        for binary_value in binary_values:
            an_integer = int(binary_value, 2)
            ascii_character = chr(an_integer)
            ascii_string += ascii_character
        return ascii_string
    except Exception:
        return "Error"


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
    return get_items(get_date_now())


@app.route("/stock/<date>")
def stock_date(date):
    return get_items(date)


def get_items(date):
    result = firebase.get(date, "")
    items = []
    if len(result.items()) == 0:
        return 'Error, try again  <a href="http://tools.wongsstudio.tk/stock/">Back</a>'
    else:
        for time, price in result.items():
            items.append(dict(name=time, description=price))
        table = ItemTable(items)
        return table.__html__()



class ItemTable(Table):
    name = Col('Time')
    description = Col('Price')


# ========================= END STOCK =============================


def get_date_now():
    country_time = datetime.now(country_time_zone)
    return country_time.strftime("%d-%m-%y")


def listToString(s):
    # initialize an empty string
    str1 = " "

    # return string
    return str1.join(s)


s = smtplib.SMTP('smtp.gmail.com', 587)

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=5000)
