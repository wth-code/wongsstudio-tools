from flask import Flask, redirect, render_template, request, flash, url_for
import smtplib

app = Flask(__name__)


@app.route("/")
def home():
    try:
        s.starttls()
        return redirect(url_for("send"))
    except Exception:
        return redirect(url_for("send"))



################   EMAIL SENDER  ########################

@app.route("/send", methods=["GET", "POST"])
def send():
    global sender_email, sender_password, sender_title, msg, li_emails
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
    return render_template("sending.html")

################   END OF EMAIL SENDER  ########################


def listToString(s):
    # initialize an empty string
    str1 = " "

    # return string
    return (str1.join(s))


s = smtplib.SMTP('smtp.gmail.com', 587)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
