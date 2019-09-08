from flask import Flask, render_template, request, url_for
import os
from workout_engine.workout_engine import get_workout

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


@app.route('/type', methods=['POST'])
def get_type():
    if request.method == 'POST':
        type_workout = request.form['type']
        print(type_workout)
        user_profile["type_workout"] = type_workout
        print(user_profile)
        return render_template("time.html")


@app.route('/time', methods=['POST'])
def get_time():
    if request.method == 'POST':
        time_workout = request.form['time']
        print(time_workout)
        user_profile["time"] = int(time_workout)
        print(user_profile)
        return render_template("mood.html")


@app.route('/mood', methods=['GET', 'POST'])
def get_mood():
    if request.method == 'POST':
        mood = request.form['mood']
        print(mood)
        user_profile["mood"] = int(mood)
        print(user_profile)
        return render_template("input.html")
    elif request.method == 'GET':
        return render_template("mood.html")

# @app.context_processor
# def utility_processor():
#     def handle_style(startpx, forloopnum):
#         return "{px}px".format(startpx + (forloopnum * 200))
#     return dict(handle_style=handle_style)

@app.route('/input', methods=['GET', 'POST'])
def get_text():
    if request.method == 'POST':
        text = request.form['text']
        print(text)
        user_profile["sentence"] = text
        print(user_profile)
        workout_dic = get_workout(user_profile)
        print("workout dict: ", workout_dic)
		# add type_workout to workout dic
        workout = {"workout": workout_dic,
		    'type_workout': user_profile['type_workout']}
        return render_template("workout.html", context=workout_dic)
    elif request.method == 'GET':
        # TESTING
        user_profile = {'type_workout': 'legs', 'time': 25,
                        'mood': 3, 'sentence': 'pretty good'}
        workout_dic = get_workout(user_profile)
        
        # add type_workout to workout dic
        workout = {"workout": workout_dic, "type_workout": user_profile['type_workout']}

        return render_template("workout.html", workout=workout)

@app.route('/realtime', methods=['GET', 'POST'])
def real_time():
    if request.method == 'POST':
		# asynchronous queries to AWS to get feedback
        pass
    elif request.method == 'GET':
        # return static
        return render_template("realtime.html")

if __name__ == '__main__':
    app.run()
