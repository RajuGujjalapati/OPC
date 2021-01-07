import time
from datetime import datetime
import traceback
from utils.mongo_initialization import Config
from utils.kairos import Kairos
import pytz
import paho.mqtt.client as mqtt
from pymongo import MongoClient
from app_config import AppConfig
from utils.general_function import *

config = Config()
config.mongo_query()
gate_ways = config.gateway_dict
device_config = config.sensor_collection
# print(device_config)
kairos = Kairos()
app_conf = AppConfig()

mongo = MongoClient(app_conf.get_mongo_host())
my_db = mongo['ilens_metadata']
my_db_live = mongo['ilens_livedata']

time_zone = config.time_zone

default = {"category_1": '', "category_2": '', "category_3": '', "category_4": '', "category_6": '', "category_7": '',
           "value": '', "previous_value": '', "last_visible": '', "timestamp": ''}

is_connected = False


def mongo_insert(raw_dict, dev_ins_id, tag_list):
    if len(raw_dict) < 1: return None
    dev_ins_id = [dev_ins_id for i in range(len(tag_list))]
    timestamp = raw_dict[0][0]
    data_list = list(zip(dev_ins_id, tag_list, raw_dict))
    result = {}
    for i in data_list:
        result.setdefault(i[0], {}).update({i[1]: i[2][1]})
    my_col = my_db_live[opc_ua_device]
    # if site_id not in my_db_live.collection_names():
    #     my_col = my_db_live[site_id]
    #     my_col.insert_one(default)
    for dev, val in result.items():
        main_doc = {

            "category_3": dev,

            "category_5": val,
        }
        data = None
        for i in my_col.find(main_doc, {"_id": 0, "value": 1, 'timestamp': 1}):
            data = i
        my_col.update_one(main_doc,
                          {
                              "$set": {"value": val, "previous_value": data.get('value') if data else None,
                                       "timestamp": timestamp
                                  , "last_visible": data.get('timestamp') if data else None},
                          },
                          upsert=True,
                          )
