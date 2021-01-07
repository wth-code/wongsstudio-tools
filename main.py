from flask import Flask, redirect, render_template, request, flash, url_for
import smtplib
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


################   EMAIL SENDER  ########################

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
            return redirect(url_for("do"))
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
            return redirect(url_for("do"))
        else:
            return render_template("send.html")


@app.route("/sending")
def do():
    try:
        s.login(sender_email, sender_password)
        for x in li_emails:
            if x == li_emails[len(li_emails) - 1]:
                s.sendmail(sender_email, x, msg)
                return render_template("sending.html", mes="Done! Your request has been done!")
            else:
                s.sendmail(sender_email, x, msg)
    except Exception:
        return render_template("sending.html", mes="Error, Try again")


################   END OF EMAIL SENDER  ########################


###########################   BMI   ############################

@app.route("/bmi", methods=["GET", "POST"])
def bmi():
    if request.method == "POST":
        num1 = request.form["num1"]
        num2_get = request.form["num2"]
        num2 = float(num2_get) / 100
        bmi = float(num1) / (float(num2) ** 2)
        return render_template("bmi.html", mes=f"Your BMI is {bmi}")
    else:
        return render_template("bmi.html")


#########################   END BMI   ###########################


#########################    COVID    ###########################

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

########################   END COVID   ###########################


@app.route("/p")
def p():
    return render_template("p.html")


def listToString(s):
    # initialize an empty string
    str1 = " "

    # return string
    return (str1.join(s))


s = smtplib.SMTP('smtp.gmail.com', 587)

if __name__ == "__main__":
    app.run(port=5000)
