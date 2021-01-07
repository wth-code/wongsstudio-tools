from flask import Flask, redirect, render_template, request, flash, url_for
import smtplib
import requests
from bs4 import BeautifulSoup
import random

app = Flask(__name__)
app.secret_key = "super secret key"

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
                        flash("Your email has been sent !")
                    else:
                        s.sendmail(sender_email, x, msg)
            except Exception:
                flash("Error, Try again")
            return render_template("send.html")
        else:
            return render_template("send.html")


################   END OF EMAIL SENDER  ########################


###########################   BMI   ############################

@app.route("/bmi", methods=["GET", "POST"])
def bmi():
    if request.method == "POST":
        num1 = request.form["num1"]
        num2_get = request.form["num2"]
        num2 = float(num2_get) / 100
        bmi = float(num1) / (float(num2) ** 2)
        flash(f"Your BMI is {bmi}")
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


######################   RANDOM NUM   ############################

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

####################   END RANDOM NUM   ##########################


####################   MORE TOOLS   ##############################

@app.route("/more")
def more():
    return render_template("more.html")

####################   END MORE TOOLS   ##########################


####################   Privacy Policy   ##########################

@app.route("/p")
def p():
    return render_template("p.html")

###################  END Privacy Policy   ########################


def listToString(s):
    # initialize an empty string
    str1 = " "

    # return string
    return (str1.join(s))


s = smtplib.SMTP('smtp.gmail.com', 587)

if __name__ == "__main__":
    app.debug = True
    app.run(port=5000)
