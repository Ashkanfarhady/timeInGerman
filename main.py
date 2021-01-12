import datetime
from constants import numbers
from flask import Flask
from flask import jsonify

app = Flask(__name__)


def get_hour_in_twelve_hour_system(hour):
    if int(hour) == 0:
        return 12
    elif int(hour) > 12:
        return hour - 12


def get_number(number):
    return numbers[get_hour_in_twelve_hour_system(number)]


def get_now():
    now = datetime.datetime.now()
    return now.hour, now.minute


def get_time_text(hour, minute):
    if minute == 0:
        return get_number(hour)
    if minute == 30:
        return "halb " + get_number(hour + 1)
    elif minute >= 25 and minute < 30:
        minute = 30 - minute
        return str(minute) + " minute vor halb " + get_number(hour + 1)
    elif minute <= 35 and minute > 30:
        minute = minute - 30
        return str(minute) + " minute nacht halb " + get_number(hour + 1)
    elif minute == 15:
        return "Viertel noch " + get_number(hour)
    elif minute == 45:
        return "viertel vor " + get_number(hour + 1)
    elif minute < 25:
        return str(minute) + " minute nach " + get_number(hour)
    elif minute < 35:
        return str(minute) + " minute nach " + get_number(hour)
    else:
        return str(60 - minute) + " minute vor " + get_number(hour + 1)


@app.route("/")
def print_time():
    hour, minute = get_now()
    try:
        response = {"status": 200, "data": f"Es ist : {get_time_text(hour, minute)}"}
    except Exception as e:
        print("Something went wront: \n", e)
        response = {"status": 500, "data": "Something went wrong with us."}
    return jsonify(response)


if __name__ == "__main__":
    app.run()
