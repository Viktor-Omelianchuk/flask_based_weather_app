"""Main module."""

import requests
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///weather.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "thisisasecret"

db = SQLAlchemy(app)


class City(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)


def get_weather_date(city):
    """The function gets weather date from 'http://api.openweathermap.org'"""

    url = (
        f"http://api.openweathermap.org/data/2.5/weather?q="
        f"{city}&units=metric&appid=6d8309305eeab8655e9b0c4ed74f5b9e"
    )
    r = requests.get(url).json()
    return r


# Views
@app.route("/")
def index_get():

    weather_data = []
    cities = City.query.all()
    for city in cities:
        r = get_weather_date(city.name)

        weather = {
            "city": city.name,
            "temperature": r["main"]["temp"],
            "description": r["weather"][0]["description"],
            "icon": r["weather"][0]["icon"],
        }

        weather_data.append(weather)

    return render_template("weather.html", weather_data=weather_data)


@app.route("/", methods=["POST"])
def index_post():
    err_msg = ""
    new_city = request.form.get("city")

    if new_city:
        existing_city = City.query.filter_by(name=new_city).first()

        if not existing_city:
            new_city_date = get_weather_date(new_city)

            if new_city_date["cod"] == 200:
                new_city_obj = City(name=new_city)
                db.session.add(new_city_obj)
                db.session.commit()
            else:
                err_msg = "City does not exists in the world!"
        else:
            err_msg = "City already exists in the database!"
    if err_msg:
        flash(err_msg, "error")
    else:
        flash("City added successfully!")

    return redirect(url_for("index_get"))


@app.route("/delete/<name>")
def delete_city(name):
    city = City.query.filter_by(name=name).first()
    db.session.delete(city)
    db.session.commit()

    flash(f"Successfully deleted { city.name }", "success")
    return redirect(url_for("index_get"))


if __name__ == "__main__":
    app.run(host="0.0.0.0")
