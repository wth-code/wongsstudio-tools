from datetime import datetime
import pytz
from flask_table import Table, Col
from firebase import firebase

country_time_zone = pytz.timezone('Asia/Hong_Kong')
country_time = datetime.now(country_time_zone)
firebase = firebase.FirebaseApplication("https://stock-3fba6-default-rtdb.firebaseio.com/", None)


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


def get():
    return get_items(
        get_date_now()) + "other dates please go to link https://wth-code-emailsender-web.zeet.app/stock/(date) date format is dd-mm-yy"
