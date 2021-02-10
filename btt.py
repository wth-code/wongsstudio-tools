from flask import request, flash, render_template


def binary_to_text():
    if request.method == "POST":
        txt_input = request.form["uin"]
        bin_done = string_to_binary(txt_input)
        flash(bin_done)
        return render_template("text_to_binary.html", txt_done=txt_input)
    else:
        flash(" ")
        return render_template("text_to_binary.html")


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
