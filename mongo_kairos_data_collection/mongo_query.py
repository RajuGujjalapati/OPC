import time

import pandas as pd
import pymongo
import pytz
from flask_pymongo import PyMongo
from flask import Flask
import datetime
from app_config import AppConfig
from pymongo import MongoClient
import calendar

app = Flask(__name__)
app_livedata = Flask(__name__)

app_conf = AppConfig()
mongo_client = app_conf.get_mongo_host()
host = mongo_client + '/'
client = MongoClient(host)
app_livedata.config['MONGO_URI'] = app_conf.get_mongo_host() + '/ilens_livedata'

# mongo = PyMongo(app)
live_app = PyMongo(app_livedata)
time_zone = 'Asia/Kolkata'
print((datetime.datetime.now() - datetime.datetime(1970, 1, 1)).total_seconds())
print(time.time())


def new_record(live_data_collection):
    return


def get_millisecond_from_date_time(date_time):
    tz = pytz.timezone('Asia/Kolkata')
    dt_with_tz = tz.localize(date_time, is_dst=None)
    seconds = (dt_with_tz - datetime.datetime(1970, 1, 1, tzinfo=pytz.UTC)).total_seconds()
    return seconds * 1000


def live_data_collection():
    now_ = datetime.datetime.now()
    diff = now_ - datetime.timedelta(minutes=1)
    print(time.time() + 600)

    lt = get_millisecond_from_date_time(now_)
    gt = get_millisecond_from_date_time(diff)
    data = pd.DataFrame(live_app.db.industry_3_client_1107.find({"timestamp": {'$lte': lt, '$gte': gt}},
                                                                {'category_7': 0, 'last_visible': 0,
                                                                 'previous_value': 0}).sort([('timestamp', -1)]))
    # pd.DataFrame(live_app.db.industry_3_client_1107.find({"timestamp": {'$lt': time.time()}},
    #                                                      {'category_7': 0, 'last_visible': 0,
    #                                                       'previous_value': 0}).sort([('timestamp', -1)]))
    data.to_csv('etst.csv')
    return data


print(live_data_collection())
