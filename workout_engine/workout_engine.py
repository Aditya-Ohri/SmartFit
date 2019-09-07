"""

Duration_Ms Type Description Pre_Sentiment_Value  => Post_Sentiment_Value

user_profile = {
   "type_workout": None,
   "time": None,
   "mood": None,
   "sentence": None,
}
"""

user_profile = {
   "type_workout": None,
   "time": None,
   "mood": 2,
   "sentence": "I love working out!",
}

import boto3
import json
import numpy as np
import uuid

comprehend_client = boto3.client("comprehend", region_name='us-east-2',
                                 aws_access_key_id=ACCESS_ID,
                                 aws_secret_access_key=ACCESS_KEY
                                 )

with open("../data/workouts.json", "r") as f:
    workouts = json.load(f)

with open("../data/ratings.json", "r") as f:
    ratings = json.load(f)

def compute_score(input_data):
    text_analyze = input_data["sentence"]
    mood_score = input_data["mood"]

    analysis = comprehend_client.detect_sentiment(Text=text_analyze, LanguageCode='en')
    text_score = analysis['SentimentScore']['Positive']

    total_score = mood_score * text_score

    return total_score


print(compute_score(user_profile))

def get_workout(input_data):
    """Returns workout given input data.
    """
    # filter by type
    filtered_input_data = list(filter(lambda x: x['type_workout'] == input_data['type_workout'], workouts))

    # get list of times
    time_list = list(map(lambda x: x['time'], filtered_input_data))

    # find workout if exists for "time", return it
    if input_data['time'] in time_list:
        # get workout that is
        workout_list = list(filter(lambda x: x['time'] == input_data['time'], time_list))

        # get ratings that correspond to workouts in workout_list
        ratings_we_want = []
        for rating in ratings:
            if rating['workout_id'] in workout_list:
                ratings_we_want.append(rating)

        # no rating exists, so just pick first
        if not ratings_we_want: 
            workout = workout_list[0]
        # grab workout with highest positive sentiment score
        else:
            workout = max(ratings_we_want, key=lambda x: x['SentimentScore']['Positive'])
    # else create a new workout with the given user time -- same attributes as workout that is CLOSEST
    else:
        # get index of workout that is closest time-wise to input_data['time']
        closest_i = np.argmin(map(lambda x: abs(x - input_data['time']), time_list))

        # new workout
        workout = filtered_input_data[closest_i]
        workout['time'] = input_data['time']

        # add new workout to data
        workouts.append(workout)
    
    return workout

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

if __name__ == '__main__':
    text="this workout was hard because I was pretty tired"
    response = comprehend_client.detect_sentiment(Text=text, LanguageCode='en')
    print(response)

    L = []
    L.append(get_workout({
        "type_workout": "cardio",
        "time": 40,
        "mood": "bad",
        "sentence": "this sucks",
    }))

    add_post_workout_rating(1, "Was awesome!")

    print("ratings****\n\n", ratings)
    print("workouts***\n\n", workouts)

    print(L)