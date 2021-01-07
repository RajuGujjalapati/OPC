"""
This program reads data from mongodb (device, tags). In this program we are reading device names at a time and fetch the
tags data, then looping through all data ( we can pass tags at a time, then we can update the data at the same time..)
"""

from opcua import Server
from opcua.common.node import Node
import time
from kairos import Kairos
import pandas as pd
from opcua import Server
import pytz
from flask_pymongo import PyMongo
from flask import Flask, jsonify
import datetime
import traceback
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
opc_server.start()
opc_server.set_server_name("FreeOpcUa Example Server")
uri = "http://examples.freeopcua.github.io"
idx = opc_server.register_namespace(uri)
# mongo = PyMongo(app)
live_app = PyMongo(app_livedata)
print(live_app)
time_zone = 'Asia/Kolkata'
kairos = Kairos()


# kairosdb_server = "opc.tcp://127.0.0.1:5019"
# kairosdb_server.start()
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


def register_service():
    data = dataframe_mongo()
    global proc, tot
    if proc == 0:
        # [opc_server.nodes.objects.add_object(idx, str(dat) ), for dat, v in data.items()]
        tot = {}
        for dat, v in data.items():
            dev = opc_server.nodes.objects.add_object(idx, str(dat))
            for j in v:
                tags = dev.add_variable(idx, j, 0)
                # print(tags)
                tot[str(j)] = tags
                tags.set_writable()
        proc += 1


def live_data():
    data = dataframe_mongo()
    for k, v in data.items():
        # print(k)
        # print(v)
        # kairos.query['metrics'] = ["category_3","category_5"]
        kairos.set_metrics_tags({"category_3": str(k), "category_5": v})
        """
        We have one options left here
        1. Don't give category_5 tags, take tags and its data by parsing the result...
        
        we have one issue as of now..
        1. If we give category_5 (all tags) at a time, eventhough the data is present in some tags, it is not providing
        data for that tags tooo.
        2. 3 tags(10074,85,89) providing more data than requested....
        
        WARNING: Resolved
        """
        # kairos.set_metrics_tags(["category_3", "category_5"])
        kairos.set_relative_time(start_time=2)
        res = kairos.get_kairos_data()
        # print(res)
        # i = 0

        for i in res:
            print(i)
            try:
                if i['group_by'][0]['group']['category_5'] in tot:
                    ref = tot[i['group_by'][0]['group']['category_5']]
                    # print((ref))
                    # ref.get_node_id()
                    # set__ = Node(opc_server,tot[i['group_by'][0]['group']['category_5']])
                    ref.set_writable()
                    ref.set_value(i['values'][0][1])
                    print(ref.get_value())
                    # print(ref)
                    # se = [(i['values'][0][1]) for i in res]

                    # print(se)
            except Exception:

                # traceback.print_exc()
                pass


proc = 0


class ListHandler:
    def __init__(self, nodes):
        self.nodes = nodes

    def list_check(self):  # pass nodes as dataframe_mongo() values not keys................
        if isinstance(self.nodes, dict):
            list_com = [[dev, tag] for dev, tag in self.nodes.items()]
            print(list_com)
        pass
        # if isinstance(self.nodes, list):
        # for device, tags in self.nodes.items():
        #     dev = opc_server.nodes.objects.add_object(idx, str(device))
        #     total_len = len(tags)
        #     while total_len:
        #         tags = dev.add_variable(idx, tags[abs(total_len - total_len)], 0)
        #         tags.set_writable()
        #         total_len -= 1
        #         print("We are class List")

# TODO: If the input is list, call this class(ListHandler) and do some preprocess...............


class TagUpdate(ListHandler):
    def __init__(self, nodes, test=None):
        super().__init__(nodes)

    def tag_mapping(self):
        pass


tg = TagUpdate(dataframe_mongo())
print(tg.list_check())

# def setting_tags_data():

proc1 = 0
while True:

    if not proc1:
        register_service()
        live_data()
        proc1 =proc1+ 1
    print("Waiting for 1 minute")
    time.sleep(60)
    live_data()
