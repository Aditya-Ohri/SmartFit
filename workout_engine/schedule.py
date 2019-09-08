# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = 'ACXXXXXXXXXXXXXXXXXXXX'
auth_token = 'XXXXXXXXXXXXXXXXXXXX'


def send_sms(number, time, exc_dic):
    client = Client(account_sid, auth_token)
    activities = [key for key in exc_dic]
    message = client.messages \
    .create(
         body='Hi there, you have a workout scheduled for ' + time + ". Here is your personalized workout plan: " + "\n"
              "1. " + str(activities[0]) + " - time: " + str(exc_dic[activities[0]]['time'])
              + ", sets: " + str(exc_dic[activities[0]]['sets']) + ", reps: " + str(exc_dic[activities[0]]['reps']) + "\n"
              "2. " + str(activities[1]) + " - time: " + str(exc_dic[activities[1]]['time'])
              + ", sets: " + str(exc_dic[activities[1]]['sets']) + ", reps: " + str(exc_dic[activities[1]]['reps']) + "\n"
              "3. " + str(activities[2]) + " - time: " + str(exc_dic[activities[2]]['time'])
              + ", sets: " + str(exc_dic[activities[2]]['sets']) + ", reps: " + str(exc_dic[activities[2]]['reps']) + "\n"
              "4. " + str(activities[3]) + " - time: " + str(exc_dic[activities[3]]['time'])
              + ", sets: " + str(exc_dic[activities[3]]['sets']) + ", reps: " + str(exc_dic[activities[3]]['reps']),
         from_='+15873161648',
         to=number
     )

    print(message.sid)

'''
send_sms('+16476857747', "9:00 PM",
         {'treadmill': {'time': '5.0 Min.', 'sets': None, 'reps': None}, 'biking': {'time': '5.0 Min.', 'sets': None, 'reps': None}, 'elliptical': {'time': '5.0 Min.', 'sets': None, 'reps': None}, 'rowing': {'time': '5.0 Min.', 'sets': None, 'reps': None}})
'''