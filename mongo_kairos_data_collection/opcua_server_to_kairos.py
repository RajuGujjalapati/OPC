import datetime
import time
from opcua import Server
# from .. import kairos_db
# from kairos_db import kairos
from kairos import Kairos
from mongo_query import get_millisecond_from_date_time
from mongo_query import live_data_collection

kairos = Kairos()
data = live_data_collection()
# kairos.set_metrics_name("ilens.raju_test")

fields = ["category_1", "category_2", "category_3", "category_4", "category_5", "category_6"]
if len(data) < 1:
    pass
else:
    for i in data:
        print(i)

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


def inserting_kairos(timestamp1=None, datapoints1=None, name1=None,val=None, *categories1):
    k_list = []
    for index, rows in data.iterrows():
        res = [rows.category_3, rows.category_6]
        for row, val in rows.value.items():
            timestamp = get_millisecond_from_date_time(datetime.datetime.now())
            if val == 0: continue
            s = {"name": "elm", "datapoints": [[timestamp, val]],
                 "tags": {"category_3": str(rows.category_3), "category_5": str(row)}}
            # response = requests.post(kairosdb_server + "/api/v1/datapoints", json.dumps(s))
            # print("Simple test [without compression]: \t%d (status code)" % response.status_code)
            k_list.append(s.copy())
            print({row: val})
        print(res)
        print('\n')

    response = requests.post(kairosdb_server + "/api/v1/datapoints", json.dumps(k_list))
    print("Simple test [without compression]: \t%d (status code)" % response.status_code)

    print(timestamp1, name1, datapoints1, categories1)

while True:
    time.sleep(60)

    inserting_kairos()
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
