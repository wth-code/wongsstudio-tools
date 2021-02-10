from flask import request, flash, render_template
import random


def rand():
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