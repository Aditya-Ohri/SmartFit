import boto3
import json
import numpy as np
import uuid
import datetime
import random
import copy


# macros
MAX_INTENSITY = 10                                  # max intensity
INTENSITY_THRESHOLD = int(MAX_INTENSITY / 3)        # allowed intensity error (e.g. intensity += 3.33)
TIME_THRESHOLD = 15                                 # allowed workout error (e.g. += 15 min)
MOOD_TO_INT = {                                     # convert mood to integer
    "happy": 5,
    "average": 3,
    "sad": 1
}


comprehend_client = boto3.client("comprehend")


with open("data/workouts.json", "r") as f:
    workouts = json.load(f)


with open("data/ratings.json", "r") as f:
    ratings = json.load(f)


def add_workout(workout):
    """Adds new workout
    """
    workouts.append(workout)
    with open("data/workouts.json", "w") as f:
        f.write(json.dumps(workouts))


def cleanse_data(input_data):
    # convert to lower text for comparison
    for k, v in input_data.items():
        # try convert to int
        try:
            input_data[k] = int(v)
        # can't convert to int, try string
        except:
            # if string
            if type(v) == str:
                # convert to lower case version
                input_data[k] = v.lower()
            else:
                raise ValueError('why is this data type not string/int')

    # convert mood to #
    input_data['mood'] = MOOD_TO_INT[input_data['mood']]


def magnitude(v):
    return np.linalg.norm(v)


def normalize(vec):
    """Normalize vector to score between 0 and WEIGHT
    """
    # compute magnitude of vector
    mag = magnitude(vec)

    # MAX size of vector is maxed inputs on every axis
    MAX_VEC_SIZE = magnitude([
        MOOD_TO_INT['happy'],
        1
    ])

    # convert to value between 0 and WEIGHT
    # divide by max possible magnitude MAX_VEC_SIZE, then multiply by 10
    return (mag * MAX_INTENSITY) / MAX_VEC_SIZE


def get_recommendation_score(input_data):
    resp = comprehend_client.detect_sentiment(
        Text=input_data['sentence'], LanguageCode='en')
    score_vec = [
        input_data['mood'],
        resp['SentimentScore']['Positive']
    ]

    return normalize(score_vec)


def get_workout(input_data):
    # cleanse data
    cleanse_data(input_data)

    # get recommendation score based on inputs
    recommendation_score = get_recommendation_score(input_data)

    # filter workout list to input type, workouts with similar intensities as recommendation scores,
    # and to appropriate time length
    def filter_type(
        workout): return workout['type'] == input_data['type_workout']
    def filter_intensities(workout): return abs(
        workout['intensity'] - recommendation_score) < INTENSITY_THRESHOLD
    def filter_times(workout): return abs(
        workout['estimated_duration'] - input_data['time']) < TIME_THRESHOLD

    # acceptable_workouts at start is just workouts
    acceptable_workouts = copy.deepcopy(workouts)

    # apply filters in order
    for f in [filter_type, filter_intensities]:
        maybe_acceptable_workouts = list(filter(f, acceptable_workouts))

        # if we filtered too much, don't set the list of acceptable workouts and break
        if len(maybe_acceptable_workouts) <= 0:
            break
        # if we filtered too only 1 workout, set list of acceptable workouts to this and break
        elif len(maybe_acceptable_workouts) == 1:
            acceptable_workouts = maybe_acceptable_workouts
            break
        # o.w., continue filtering
        else:
            acceptable_workouts = maybe_acceptable_workouts

    # for time filtering
    times = map(lambda workout: workout['estimated_duration'], acceptable_workouts)
    if input_data['time'] not in times:
        # get index of workout that is closest time-wise to input_data['time']
        closest_i = np.argmin(map(lambda x: abs(x - input_data['time']), times))

        # new workout
        workout = copy.deepcopy(acceptable_workouts[closest_i])
        workout['intensity'] = int(recommendation_score)
        workout['estimated_duration'] = input_data['time']
        workout['id'] = str(uuid.uuid4())

        print("NEW WORKOUT: ", workout)
        add_workout(workout)
        return workout

    # return random choice within acceptable workout list
    return random.choice(acceptable_workouts)

def add_post_workout_rating(workout_id, rating):
    """Adds new rating for workout_id with text 'rating'
    """
    resp = comprehend_client.detect_sentiment(
        Text=rating, LanguageCode='en')
    ratings.append({
        "workout_id": workout_id,
        "id": uuid.uuid4(),
        "post_sentiment_value": resp['Sentiment'],
        "SentimentScore": resp['SentimentScore']
    })


if __name__ == '__main__':
    L = []
    L.append(get_workout({
        "type_workout": "cardio",
        "time": 40,
        "mood": "Happy",
        "sentence": "I am happy",
    }))

    print("Recommended workout: ", L)
