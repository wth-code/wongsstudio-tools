# MODULES
from flask import *
import multiprocessing
# FILES
import emailSend
import bmi_calculator
import covid_virus
import randnum
import btt
import ytthumb
import stock_ui
from weather import get_weather
from stock import get_stock

app = Flask(__name__)
app.secret_key = "super secret key"


@app.route("/")  # HOME
def home():
    return render_template("index.html")


@app.route("/send", methods=["GET", "POST"])  # MULTIPLE EMAIL SENDER
def send():
    return emailSend.send()


@app.route("/bmi", methods=["GET", "POST"])  # BMI CALCULATOR
def bmi():
    return bmi_calculator.calculate()


@app.route("/covid", methods=["GET", "POST"])  # COVID 19 DATA
def covid():
    return covid_virus.grab_info()


@app.route("/rand_num", methods=["GET", "POST"])  # RANDOM NUMBER GENERATOR
def rad_num():
    return randnum.rand()


@app.route("/ytthumb", methods=["GET", "POST"])  # YOUTUBE THUMBNAIL
def yt():
    return ytthumb.get_thumb()


@app.route("/text_to_binary", methods=["GET", "POST"])  # BINARY TO TEXT
def binary_to_text():
    return btt.binary_to_text()


@app.route("/binary_to_text", methods=["GET", "POST"])  # TEXT TO BINARY
def text_to_binary():
    return btt.text_to_binary()


@app.route("/more")  # MORE TOOLS
def more():
    return render_template("more.html")


@app.route("/p")  # Privacy Policy
def p():
    return render_template("p.html")


@app.route("/stock")  # STOCK TODAY
def stock_web():
    return stock_ui.get()


@app.route("/stock/<date>")  # STOCK WITH DATE
def stock_date(date):
    return stock_ui.get_items(date)

if __name__ == "__main__":
    # multiprocessing.Process(target=get_weather.doit).start()
    # multiprocessing.Process(target=get_stock.get_now).start()
    app.debug = True
    app.run()
