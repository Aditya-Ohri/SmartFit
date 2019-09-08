import boto3
from base64 import b64decode
import re

ACCESS_ID = "XXXXXXXXXXXXXXXXXXXXXXX"
ACCESS_KEY = "XXXXXXXXXXXXXXXX"

# Create SDK clients for rekognition
rekog_client = boto3.client("rekognition", region_name='us-east-2',
                                 aws_access_key_id=ACCESS_ID,
                                 aws_secret_access_key=ACCESS_KEY)


def bytes_to_img(imageBytes):
    # sub out the damn metadata
    imgdata = re.sub('^data:image/.+;base64,', '', imageBytes)

    # decode bytes
    imgdata = b64decode(imgdata)

    return imgdata

feedback_list = {
    "HAPPY": "Keep up the good work! You're killing it!",
    "FEAR": "I know this is hard, but you're doing great.",
    "ANGRY": "Suck it up, buttercup. (I need a little tough love every now and then.)",
    "DISGUSTED": "Maybe take a quick break.",
    "CALM": "You seem a bit bored. Let's pick up the effort a little bit."
}

def feedback(aws_resp):
    # sort emotions
    emotions = sorted(
        aws_resp['FaceDetails'][0]['Emotions'],
        key=lambda e: ['Confidence'],
        reverse=True
    )

    # TODO > this needs work
    try:
        # fow now, just return response for highest predicted emotion
        highest_predicted_emotion = feedback_list[emotions[0]['Type']]
        print("Highest predicted emotion: ", emotions[0]['Type'].lower())
        return highest_predicted_emotion
    except KeyError:
        return "Dig deep. You can do this."

def analyze_face(imageBytes):
    # convert bytes to image
    im = bytes_to_img(imageBytes)

    # pass to AWS API
    response = rekog_client.detect_faces(
        Image={ 'Bytes': im },
        Attributes=['ALL']
    )

    # get feedback intelligently
    # TODO > store this data and compare to their actual textual feedback
    # utilize that feedback to make model better and improve feedback given to user
    feedback_response = {
        "feedback": feedback(response)
    }
    return feedback_response
