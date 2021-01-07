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

web_mqtt_client = mqtt.Client(transport="websockets", )
mqtt_host, mqtt_port = app_conf.get_web_socket_host()

is_connected = False

trial = 1
if trial <= 3:
    while not is_connected:
        try:
            web_mqtt_client.connect(mqtt_host, mqtt_port, 60)
            web_mqtt_client.loop_start()
            print('connected websocket')
            is_connected = True
        except Exception as e:
            traceback.print_exc()
            print('not able to connect websocket', e)
            trial = trial + 1
            # time.sleep(3)


def get_millisecond_from_date_time(date_time):
    tz = pytz.timezone(time_zone)
    dt_with_tz = tz.localize(date_time, is_dst=None)
    seconds = (dt_with_tz - datetime(1970, 1, 1, tzinfo=pytz.UTC)).total_seconds()
    return seconds * 1000


def mongo_insert(raw_dict, dev_ins_id, tag_list, site_id, gateway_instance, sensor_id, block_id):
    if len(raw_dict) < 1: return None
    dev_ins_id = [dev_ins_id for i in range(len(tag_list))]
    timestamp = raw_dict[0][0]
    data_list = list(zip(dev_ins_id, tag_list, raw_dict))
    result = {}
    for i in data_list:
        result.setdefault(i[0], {}).update({i[1]: i[2][1]})
    my_col = my_db_live[site_id]
    if site_id not in my_db_live.collection_names():
        my_col = my_db_live[site_id]
        my_col.insert_one(default)
    for dev, val in result.items():
        main_doc = {
            "category_1": site_id,
            "category_2": gateway_instance,
            "category_3": dev,
            "category_4": "block_" + str(block_id),
            "category_6": sensor_id,
            "category_7": "",
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


def process_pay(x):
    try:
        print(x)
        t = time.time()
        x = json.loads(x)
        raw_int = x.get('values')
        tag_list = x.get('tag_list')
        x_timestamp = x.get('timestamp')

        asset = device_config.get(x['gateway_id']).get(x['com_id']).get(x['block']).get('dev_list')
        if asset is None: return None
        for device_ins_id, instance_id in asset.items():
            # raw_list, tag_list = ([], [])
            if 'float_' in instance_id.keys():
                mul_list = instance_id.get('float_').get('mul_list')
                # mapped_val, tags = reg_map(raw_int, instance_id.get('float_').get('add_list'),
                #                            instance_id.get('float_').get('tag_list'))
                # raw_val = process_raw_data(UINT16toFLOAT32, mapped_val, mul_list, x_timestamp, False)
                # if raw_val:
                #     raw_list.extend(raw_val)
                #     tag_list.extend(tags)
            # tag_list.extend(tags)
            if raw_int: # list of values
                raw_list = list(map(lambda x: [x_timestamp, x], raw_int))
                print("rawlisttttttttttttttttttt", raw_list) # timestamp with values
                raw_list.extend([[x_timestamp, x['tag_100081']]])

            tag_list.append('tag_100081')
            print(tag_list)

            print(raw_int)
            kairos_list = structure_query(raw_list, x['industry_id'], x['gateway_id'], device_ins_id, x['block'],
                                          tag_list,
                                          x['sensor_id'])
            kairos.update_kairos_data(True, kairos_list)
            mongo_insert(raw_list, device_ins_id, tag_list, x['industry_id'], x['gateway_id'], x['sensor_id'],
                         x['block'])
            web_socket_struct(raw_list, device_ins_id, tag_list, x['industry_id'], x['gateway_id'], x['sensor_id'],
                              x['block'], web_mqtt_client)
            print('time->>', device_ins_id, x['gateway_id'], time.time() - t)
            time.sleep(0.2)
    except Exception:
        traceback.print_exc()
        print(x)
