import json

from flask import Flask, render_template, redirect, request, jsonify
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, SelectMultipleField
from wtforms.validators import DataRequired, Email, Length
import datetime
from flask_sqlalchemy import SQLAlchemy
import smtplib
import os

OWN_EMAIL = "dkritsas2002@gmail.com"
OWN_PASSWORD = "wreydhyuxotnykil"

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "sth here")
Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL1", "sqlite:///meetings.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class MeetingDate(db.Model):
    date = db.Column(db.String(16))
    time = db.Column(db.Integer)
    id = db.Column(db.String, primary_key=True)


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    time_list = get_meetings(str(datetime.date.today()))
    disabled = []
    for time in time_list:
        if time == "True":
            disabled.append('disabled=True')
        else:
            disabled.append('')
    print(disabled)

    return render_template("index.html", times=time_list, disabled=disabled)


def check_if_date_exists_in_db(date):
    find_date = MeetingDate.query.get(date)
    db.session.commit()
    print(find_date)
    if not find_date:
        print("NULL")

    return find_date


def get_meetings(date):
    times = ["9:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00"]
    available = []

    meeting_hours = MeetingDate.query.filter_by(date=date).all()

    for i in range(len(times)):
        j = 0
        if j < len(meeting_hours) and times[i] == meeting_hours[j].time:

            available.append("True")
            j += 1
        else:
            available.append("False")

    print(available)
    return available



@app.route("/datepicker", methods=["POST", "get"])
def datepicker():
    write = 0


    print(request.method)
    if request.method == "POST":
        date = request.form["date"]
        times = get_meetings(date)

        get_meetings(date)
        # if not check_if_date_exists_in_db(date):
        #
        #     # today = datetime.datetime.now()
        #     new_meeting = MeetingDate(date=date)
        #     db.session.add(new_meeting)
        #     db.session.commit()

        return jsonify({"times": times})

    return jsonify({"error": "No times available"})


def send_email(email, phone_number, date, time):
    email_message = f"Subject:New Client\n\nDate: {date}\nTime: {time}\n" \
                    f"Client Email: {email}\nClient phone Number: {phone_number}"

    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(OWN_EMAIL, OWN_PASSWORD, )
        connection.sendmail(OWN_EMAIL, OWN_EMAIL, email_message)


# book meeting and send email
@app.route("/submit_meeting", methods=["POST"])
def submit_meeting():
    if request.method == "POST":
        date = request.form.get("date", False)
        time = request.form.get("time", False)
        email = request.form.get("email", False)
        phone_number = request.form.get("phone_number", False)

        date_time = date + "-" + str(time)

        new_meeting = MeetingDate(date=date, time=time, id=date_time)
        db.session.add(new_meeting)
        db.session.commit()

        # check if client entered email of phone number
        if email == "" and phone_number == "":
            return jsonify({"error": "No contact info given"})

        send_email(email, phone_number, date, time)

        return jsonify({"Success": "Success"})
    return jsonify({"error": "error"})


if __name__ == "__main__":
    app.run(debug=True)
