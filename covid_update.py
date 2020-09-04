import tweepy
import time
import requests
# NOTE: I put my keys in the keys.py to separate them
# from this main file.
# Please refer to keys_format.py to see the format.
from keys import *
from datetime import datetime

# NOTE: flush=True is just for running this script
# with PythonAnywhere's always-on task.
# More info: https://help.pythonanywhere.com/pages/AlwaysOnTasks/
print('Twitter Bot', flush=True)

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

FILE_NAME = 'last_seen_date.txt'

def retrieve_last_seen_date(file_name):
     f_read = open(file_name, 'r')
     last_seen_date = str(f_read.read().strip())
     f_read.close()
     return last_seen_date

def store_last_seen_date(last_seen_date, file_name):
     f_write = open(file_name, 'w')
     f_write.write(str(last_seen_date))
     f_write.close()
     return

def check_realtime_cases():
    now = datetime.now()
    date_from = now.strftime("%Y-%d-%mT") #Output 2020-04-09T
    date_to = now.strftime("%Y-%d-%mT") #Output 2020-04-09T
    url="https://api.covid19api.com/country/venezuela/status/confirmed/live?from={}&to={}".format(date_from+"00:00:00Z", date_to+"23:59:59Z")
    response = requests.get(url)
    r_dictionary= response.json()
    return(r_dictionary)

def posting_covid_status():
    print('POSTING COVID Status...', flush=True)
    now = datetime.now().strftime("%Y-%d-%m")

    #Checking the EndPoint for extrat the data
    today_cases = check_realtime_cases()
    cases = today_cases[0]["Cases"]

    #Post template
    post= "#ReporteCOVID para el dia de hoy {}, En: Venezuela, Casos de HOY: {} Confirmados. #COVID2020 - Fuente: Johns Hopkins University https://coronavirus.jhu.edu/map.html".format(now, cases)
    print(post, flush=True)

    #last date stored
    last_seen_date = retrieve_last_seen_date(FILE_NAME)
    print("Last Date",last_seen_date)

    if last_seen_date != now:
        #send tweet
        api.update_status(post)
        #store last reporting date
        store_last_seen_date(now, FILE_NAME)
        print('Posting Done', flush=True)


while True:
    posting_covid_status()
    #Execute every 10 hours
    time.sleep(36000)
