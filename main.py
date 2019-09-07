from flask import Flask, render_template, request, url_for
import os
#from workout_engine.workout_engine import get_workout

app = Flask(__name__)

user_profile = {
    "type_workout": None,
    "time": None,
    "mood": None,
    "sentence": None,
}

@app.route('/')
def home():
    return render_template("type.html")


@app.route('/type', methods = ['POST'])
def get_type():
    if request.method == 'POST':
        type_workout = request.form['type']
        print(type_workout)
        user_profile["type_workout"] = type_workout
        print(user_profile)
        return render_template("time.html")


@app.route('/time', methods = ['POST'])
def get_time():
    if request.method == 'POST':
        time_workout = request.form['time']
        print(time_workout)
        user_profile["time"] = int(time_workout)
        print(user_profile)
        return render_template("mood.html")


@app.route('/mood', methods = ['POST'])
def get_mood():
    if request.method == 'POST':
        mood = request.form['mood']
        print(mood)
        user_profile["mood"] = mood
        print(user_profile)
        return render_template("input.html")


@app.route('/input', methods = ['POST'])
def get_text():
    if request.method == 'POST':
        text = request.form['text']
        print(text)
        user_profile["sentence"] = text
        print(user_profile)
        return text


if __name__ == '__main__':
    app.run()