"""

Duration_Ms Type Description Pre_Sentiment_Value  => Post_Sentiment_Value

user_profile = {
   "type_workout": None,
   "time": None,
   "mood": None,
   "sentence": None,
}

user_profile = {'type_workout': 'cardio', 'time': 20, 'mood': 3, 'sentence': 'I love working out!'}
"""


import boto3
import json
import numpy as np
import uuid

ACCESS_ID = "XXXXXX"
ACCESS_KEY = "XXXXXX"
comprehend_client = boto3.client("comprehend", region_name='us-east-2',
                                 aws_access_key_id=ACCESS_ID,
                                 aws_secret_access_key=ACCESS_KEY
                                 )


with open("data/workouts.json", "r") as f:
    workouts = json.load(f)
    print(workouts)

with open("data/ratings.json", "r") as f:
    ratings = json.load(f)


def compute_score(input_data):
    text_analyze = input_data["sentence"]
    mood_score = input_data["mood"]

    analysis = comprehend_client.detect_sentiment(Text=text_analyze, LanguageCode='en')
    text_score = analysis['SentimentScore']['Positive']

    total_score = mood_score * text_score

    return total_score


#print(compute_score(user_profile))


def get_workout(input_data):
    score = compute_score(input_data)
    time = input_data['time']
    print(time)
    type_workout = input_data['type_workout']
    print(type_workout)
    for i in range(len(workouts)):
        print(workouts[i]['type_workout'])
        if workouts[i]['type_workout'] == type_workout:
            category_df = workouts[i]
    if score < 1:
        narrowed_df = category_df['workouts'][0]['activities']
    elif 1 <= score < 2:
        narrowed_df = category_df['workouts'][1]['activities']
    else:
        narrowed_df = category_df['workouts'][2]['activities']
    for key in narrowed_df:
        print(narrowed_df[key])
        narrowed_df[key] = time * narrowed_df[key]
    print(narrowed_df)
    if type_workout == "cardio":
        for key in narrowed_df:
            narrowed_df[key] = {"time": str(narrowed_df[key]) + " Min.", "sets": "N/A", "reps": "N/A"}
        return narrowed_df
    else:
        for key in narrowed_df:
            narrowed_df[key] = {"time": str(narrowed_df[key]) + " Min.", "sets": str(round(narrowed_df[key] * 2/5)), "reps": 10}
        return narrowed_df


#print(get_workout(user_profile))


def add_post_workout_rating(workout_id, rating):
    """Adds new rating for workout_id with text 'rating'
    """
    try:
        resp = comprehend_client.detect_sentiment(Text=rating, LanguageCode='en')
        ratings.append({
            "workout_id": workout_id,
            "id": uuid.uuid4(),
            "post_sentiment_value": resp['Sentiment'],
            "SentimentScore": resp['SentimentScore']
        })
    except:
        pass


def suggest_workout():
    """
    
    """
    pass

