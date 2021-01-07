import traceback

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

kairosdb_server = "http://192.168.4.95:18085"
def dataframe_mongo():
    data = pd.DataFrame(live_app.db.opc_ua_device.find({}))
    return data
# print(data)
opc_server.start()
kairos.set_metrics_name('ilens.live_data.raw')


def get_millisecond_from_date_time(date_time):
    tz = pytz.timezone('Asia/Kolkata')
    dt_with_tz = tz.localize(date_time, is_dst=None)
    seconds = (dt_with_tz - datetime.datetime(1970, 1, 1, tzinfo=pytz.UTC)).total_seconds()
    return seconds * 1000


proc = 0


def whole_process(dat=None, tags_id=None, data=[]):
    global proc

    for col, dat in data.iterrows():
        print(col)
        tags_id = [_['tag_id'] for _ in dat.tagsData]
        print(tags_id)
        # dev = dat.device_instance_id
        # print(dev)

        if proc == 0:
            global dev, tag, total_data, final_tag, tagnode_tag_id
            dev = opc_server.nodes.objects.add_object(idx, str(dat.device_instance_id))
            final_tag = {}
            tagnode_tag_id = {}

            for tag_ in tags_id:

                tag = dev.add_variable(idx, str(tag_), 0)
                tagnode_tag_id[tag_] = tag

                print(tag, type(tag), tag.get_properties())
                tag.set_writable()
                kairos.set_metrics_tags({"category_3": [str(dat.device_instance_id)], "category_5": [str(tag_)]})
                kairos.set_relative_time(start_time=random.randint(1, 5), unit='minutes')
                # kairos.set_start_end_date(True, gt, lt)
                # response = requests.post(kairosdb_server + "/api/v1/datapoints", json.dumps([kairos.query]))
                # print(response)
                res = kairos.get_kairos_data()
                print(res)
                try:
                    total_data = res[0]['values'][0][1]
                    if total_data:
                        kairos_tag_id = res[0]['group_by'][0]['group']['category_5']
                        tag.set_value(total_data)
                        final_tag[kairos_tag_id] = total_data
                        print(total_data)
                except (IndexError, KeyError):
                    traceback.print_exc()
                    pass


        else:
            dev = dev
            for tag_ in tags_id:
                if tag_ in final_tag:
                    tag = tagnode_tag_id[tag_]
                    kairos.set_metrics_tags({"category_3": [str(dat.device_instance_id)], "category_5": [str(tag_)]})
                    kairos.set_relative_time(start_time=10, unit='minutes')
                    # kairos.set_start_end_date(True, gt, lt)
                    # response = requests.post(kairosdb_server + "/api/v1/datapoints", json.dumps([kairos.query]))
                    # print(response)
                    res = kairos.get_kairos_data()
                    print(res)
                    try:
                        total_data = res[0]['values'][0][1]
                        if total_data:
                            kairos_tag_id = res[0]['group_by'][0]['group']['category_5']
                            "Replace tag_name with node_id"
                            tag.write_value(total_data)
                            final_tag[kairos_tag_id] = total_data
                            print(total_data)
                    except Exception:
                        traceback.print_exc()
                        pass

        # kairos.set_metrics_tags({"category_3": [str(dat.device_instance_id)], "category_5": [str(tags_id)]})
        # kairos.set_relative_time(start_time=random.randint(1, 5), unit='minutes')
        # # kairos.set_start_end_date(True, gt, lt)
        # response = requests.post(kairosdb_server + "/api/v1/datapoints", json.dumps([kairos.query]))
        # print(response)
        # res = kairos.get_kairos_data()
        # total_data = res[0]['values']
        # print(total_data)
        # global tag
        # tag = dev.add_variable(idx, str(tags_id), 0)
        # now_ = datetime.datetime.now()
        # diff = now_ - datetime.timedelta(minutes=2100)
        # lt = get_millisecond_from_date_time(now_)
        # gt = get_millisecond_from_date_time(diff)

        # tags_id = [_['tag_id'] for _ in dat.tagsData]
        #
        # if str(tag) in tags_id:
        #     print(tag)

        # if not total_data:
        #
        #     tag = dev.add_variable(idx, str(tags_id), None)
        #     tag.set_writable()
        # else:
        #     tag.set_value(total_data[0][1])
        #     print(tag.get_value())
    proc += 1
    print("We are waiting for one minute")
    print(final_tag)
    time.sleep(6)
    # return str(dat.device_instance_id), tags_id


"plan is to store all tag names and loop  through the tags and assign values to it."

'But if we do that again its going to create same tag for every new value(which is not good) in our case'

' But a'


def process_for_kairos_extraction(tag_id):
    kairos.set_metrics_name('ilens.live_data.raw')
    kairos.set_metrics_tags({"category_3": [str(dat.device_instance_id)], "category_5": [str(tags_id)]})
    kairos.set_relative_time(start_time=random.randint(1, 5), unit='minutes')
    # kairos.set_start_end_date(True, gt, lt)
    response = requests.post(kairosdb_server + "/api/v1/datapoints", json.dumps([kairos.query]))
    print(response)
    res = kairos.get_kairos_data()
    total_data = res[0]['values']
    print(total_data)
    global tag
    tag = dev.add_variable(idx, str(tags_id), 0)

    """if tag in tags_id:
    tag.set_value(9000)
    """


if __name__ == '__main__':
    while True:
        whole_process(data = dataframe_mongo())
        time.sleep(60)
