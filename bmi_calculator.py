from flask import request, flash, render_template


def calculate():
    if request.method == "POST":
        num1 = request.form["num1"]
        num2_get = request.form["num2"]
        num2 = float(num2_get) / 100
        bmi = float(num1) / (float(num2) ** 2)
        flash(f"Your BMI is {bmi}")
    return render_template("bmi.html")