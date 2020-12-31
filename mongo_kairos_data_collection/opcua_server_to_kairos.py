import datetime
import time
from opcua import Server

from kairos import Kairos
from mongo_query import get_millisecond_from_date_time
from mongo_query import live_data_collection

kairos = Kairos()
data = live_data_collection()
# kairos.set_metrics_name("ilens.raju_test")

fields = ["category_1", "category_2", "category_3", "category_4", "category_5", "category_6"]
if len(data) < 1:
    pass
# else:
#     for i in data:
#         print(i)

# data = [
#     {
#         "name": "test",
#         "datapoints": [
#             [1359788400000, 123],
#             [1359788300000, 13.2],
#             [1359788410000, 23.1]
#         ],
#         "tags": {
#             "project": "rola"
#         }
#     }
# ]

import requests
import json
import gzip

kairosdb_server = "http://192.168.4.90:18080"
opc_server = Server()
opc_server.set_endpoint(url="opc.tcp://127.0.0.1:5091")
opc_server.set_server_name("FreeOpcUa Example Server")

# set all possible endpoint policies for clients to connect through

# setup our own namespace
uri = "http://examples.freeopcua.github.io"
idx = opc_server.register_namespace(uri)
def tag_data():
    all_devices_list=['1','a','w']
    for dev in all_devices_list:
        print(dev)
        for  val in data['value']:
            print(val)
            # tag = dev.add_variable(idx, str(row), val)
            # print(tag.get_value())
            # tag.set_writable()
tag_data()

            # timestamp = get_millisecond_from_date_time(datetime.datetime.now())
            # # if val == 0 or None: continue
            # s = {"name": "elm", "datapoints": [[timestamp, val]],
            #      "tags": {"category_3": str(rows.category_3), "category_5": str(row)}}
            # tag = dev.add_variable(f'ns={idx};s={str(row)}+{str(rows.category_3)}', str(row), val)#.set_modelling_rule(True) #getting error if we use  modelling...
            # tag = dev.add_variable(idx, str(row), val)
            # print(tag.get_value())
            # tag.set_writable()
            # response = requests.post(kairosdb_server + "/api/v1/datapoints", json.dumps(s))
            # print("Simple test [without compression]: \t%d (status code)" % response.status_code)
            # k_list.append(s.copy())
            # print({row: val})
all_devices_list = []
def device_handler(data,timestamp1=None, datapoints1=None, name1=None,val=None, *categories1):
    k_list = []
    for index, rows in data.iterrows():
        res = [rows.category_3, rows.category_6]
        # dev = opc_server.nodes.base_object_type.add_object_type(idx, str(rows.category_3))  ############## learn test_modelling_rule
        if rows.category_3 in all_devices_list:
            tag_data()
        dev = opc_server.nodes.objects.add_object(idx, str(rows.category_3))
        print(dev)
        for row, val in rows.value.items():
            print(val)
            timestamp = get_millisecond_from_date_time(datetime.datetime.now())
            # if val == 0 or None: continue
            s = {"name": "elm", "datapoints": [[timestamp, val]],
                 "tags": {"category_3": str(rows.category_3), "category_5": str(row)}}
            # tag = dev.add_variable(f'ns={idx};s={str(row)}+{str(rows.category_3)}', str(row), val)#.set_modelling_rule(True) #getting error if we use  modelling...
            tag = dev.add_variable(idx, str(row), val)
            print(100*'*',type(tag))
            tag.set_writable()
            # response = requests.post(kairosdb_server + "/api/v1/datapoints", json.dumps(s))
            # print("Simple test [without compression]: \t%d (status code)" % response.status_code)
            k_list.append(s.copy())
            print({row: val})
        print(res)
        # print('\n')

    response = requests.post(kairosdb_server + "/api/v1/datapoints", json.dumps(k_list))
    print("Simple test [without compression]: \t%d (status code)" % response.status_code)

    # print(timestamp1, name1, datapoints1, categories1)
test =0
opc_server.start()
while True:
    if test == 0:
        device_handler(data = live_data_collection())
        test+=1

    time.sleep(60)
    device_handler(data = live_data_collection())



    print("Process Completed")









# kairos.update_kairos_data(k_list[1:20])

# sec = kairos.set_metrics_tags({"category_10": [str(data['catergory_3'])], "category_6": [data['catergory_6']], "value": data['value']})
# print(sec)

# kairos.set_start_end_date(True, start_millisecond, end_millisecond)
# kairos.set_metrics_aggregators([
#         {
#           "name": "sum",
#           "sampling": {
#             "value": "1",
#             "unit": "milliseconds"
#           }
#         }
#       ])
# response = []
#
#


#
#
# response = requests.post(kairosdb_server + "/api/v1/datapoints", json.dumps(k_list))
# print("Simple test [without compression]: \t%d (status code)" % response.status_code )

#
# device_list = []
# if devic_id in device_list:
#     pass
# dev = opc_server.nodes.base_object_type.add_object_type(idx, str(rows.category_3))

def default_kairos_process(data,timestamp1=None, datapoints1=None, name1=None,val=None, *categories1):
    k_list = []
    all_devices_list = []
    for index, rows in data.iterrows():
        res = [rows.category_3, rows.category_6]
        # dev = opc_server.nodes.base_object_type.add_object_type(idx, str(rows.category_3))  ############## learn test_modelling_rule
        if rows.category_3 in all_devices_list:
            pass
        dev = opc_server.nodes.objects.add_object(idx, str(rows.category_3))
        print(dev)
        for row, val in rows.value.items():
            print(val)
            timestamp = get_millisecond_from_date_time(datetime.datetime.now())
            # if val == 0 or None: continue
            s = {"name": "elm", "datapoints": [[timestamp, val]],
                 "tags": {"category_3": str(rows.category_3), "category_5": str(row)}}
            # tag = dev.add_variable(f'ns={idx};s={str(row)}+{str(rows.category_3)}', str(row), val)#.set_modelling_rule(True) #getting error if we use  modelling...
            tag = dev.add_variable(idx, str(row), val)
            # print(tag.get_value())
            tag.set_writable()
            # response = requests.post(kairosdb_server + "/api/v1/datapoints", json.dumps(s))
            # print("Simple test [without compression]: \t%d (status code)" % response.status_code)
            k_list.append(s.copy())
            print({row: val})
        print(res)
        # print('\n')

    response = requests.post(kairosdb_server + "/api/v1/datapoints", json.dumps(k_list))
    print("Simple test [without compression]: \t%d (status code)" % response.status_code)

    # print(timestamp1, name1, datapoints1, categories1)
test =0
opc_server.start()
while True:
    if test == 0:
        inserting_kairos(data = live_data_collection())
        test+=1

    time.sleep(60)
    inserting_kairos(data = live_data_collection())



    print("Process Completed")