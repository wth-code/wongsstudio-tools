import smtplib
from flask import request, flash, render_template

s = smtplib.SMTP('smtp.gmail.com', 587)


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