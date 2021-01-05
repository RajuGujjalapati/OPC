"""
This program reads data from mongodb (device, tags). In this program we are reading device names at a time and fetch the
tags data, then looping through all data ( we can pass tags at a time, then we can update the data at the same time..)
"""

from opcua import Server

import time
from kairos import Kairos
import pandas as pd
from opcua import Server
import pytz
from flask_pymongo import PyMongo
from flask import Flask, jsonify
import datetime
from app_config import AppConfig
from pymongo import MongoClient
import requests, json
import random

# app = Flask(__name__)
app_livedata = Flask(__name__)

app_conf = AppConfig()
mongo_client = app_conf.get_mongo_host()
host = mongo_client + '/'
client = MongoClient(host)
app_livedata.config['MONGO_URI'] = app_conf.get_mongo_host() + '/ilens_metadata'
opc_server = Server()
opc_server.set_endpoint(url="opc.tcp://127.0.0.1:5091")
opc_server.set_server_name("FreeOpcUa Example Server")
uri = "http://examples.freeopcua.github.io"
idx = opc_server.register_namespace(uri)
# mongo = PyMongo(app)
live_app = PyMongo(app_livedata)
print(live_app)
time_zone = 'Asia/Kolkata'
kairos = Kairos()


# kairosdb_server = "http://192.168.4.95:18085"
def dataframe_mongo():
    data = pd.DataFrame(live_app.db.opc_ua_device.find({}))

    # 1st approach
    # print(data.loc['category_3'])
    tags_id = [thi['tag_id'] for k in data.tagsData for thi in k]
    # print(tags_id)

    # 2nd approach!!!!!!!
    final_data = {}
    for col, dat in data.iterrows():
        # print(col)
        print(dat.device_instance_id)
        tags_id = [_['tag_id'] for _ in dat.tagsData]
        final_data[dat.device_instance_id] = tags_id
        # print(tags_id)
    return final_data


kairos.set_metrics_name('ilens.live_data.raw')


def live_data():
    data = dataframe_mongo()
    for k, v in data.items():
        print(k)
        print(v)
        # kairos.query['metrics'] = ["category_3","category_5"]
        kairos.set_metrics_tags({"category_3": str(k), "category_5":v})
        """
        We have one options left here
        1. Don't give category_5 tags, take tags and its data by parsing the result...
        
        we have one issue as of now..
        1. If we give category_5 (all tags) at a time, eventhough the data is present in some tags, it is not providing
        data for that tags tooo.
        2. 3 tags(10074,85,89) providing more data than requested....
        """
        # kairos.set_metrics_tags(["category_3", "category_5"])
        kairos.set_relative_time(start_time=10)
        res = kairos.get_kairos_data()
        print(res)
        i = 0
        try:
            se = [(i['group_by'][0]['group']['category_5'], i['values']) for i in res];print(se)
        except Exception:
            pass


while True:
    proc = True
    if proc:
        live_data();
        proc = False
    time.sleep(30)
    live_data()
