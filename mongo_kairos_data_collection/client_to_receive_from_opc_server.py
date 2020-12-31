import time

import pytz
from opcua import Client
from kairos import Kairos
from flask import Flask
from app_config import AppConfig
from flask_pymongo import PyMongo
import pandas as pd
import datetime

app_metadata = Flask(__name__)

app_conf = AppConfig()
mongo_client = app_conf.get_mongo_host()
host = mongo_client + '/'
# client = MongoClient(host)
app_metadata.config['MONGO_URI'] = app_conf.get_mongo_host() + '/ilens_metadata'

# mongo = PyMongo(app)
meta_data_app = PyMongo(app_metadata)
time_zone = 'Asia/Kolkata'
kairos = Kairos()
client = Client(url="opc.tcp://127.0.0.1:5091")
client.connect()


def get_millisecond_from_date_time(date_time):
    tz = pytz.timezone('Asia/Kolkata')
    dt_with_tz = tz.localize(date_time, is_dst=None)
    seconds = (dt_with_tz - datetime.datetime(1970, 1, 1, tzinfo=pytz.UTC)).total_seconds()
    return seconds * 1000


def live_data():
    obj = client.get_objects_node().get_children()[1:]
    obj = [i.get_children() for i in obj]
    for _ in obj:
        for i in _:
            try:
                s = i.get_value()
                name = i.get_browse_name()
                print(s, name)
            except Exception:
                pass


"Try to make seperate services for live and log data........" \
"As of now our target is to give historical data at only once. If we hit the historical log data at once we can then \
 fetch live data then!"


def log_data():  # device_id, start_date, end_date, status
    # if start_date or end_date or status is None:
    #     raise Exception("Please fill the required fields!!!!")
    # kairos.set_metrics_name('ilens.live_data.raw')
    # kairos.set_metrics_tags({"category_3": device_id})
    # # Not working with set_start_end_date function
    # # use set_relative instead
    #
    # # print(time.time() + 600)
    #
    # lt = get_millisecond_from_date_time(now_)
    # gt = get_millisecond_from_date_time(diff)
    # kairos.set_start_end_date(status, start_date, end_date)
    mongo_return = meta_data_app.db.opc_ua_device.find({})
    data = pd.DataFrame(meta_data_app.db.opc_ua_device.find({}))
    for i in mongo_return:
        if i['category'] == "live":
            print(end='\n')
            live_data()
        else:
            log_data()


now_ = datetime.datetime.now()
diff = now_ - datetime.timedelta(minutes=6)
if __name__ == '__main__':
    # while True:
    # time.sleep(5)
    # live_data()
    log_data()
