from opcua import Client
from kairos import Kairos
import pytz
import datetime
import time, requests
import json

kairosdb_server = "http://192.168.4.95:18085"

kairos = Kairos()


# opc_server = Server()
# opc_server.set_endpoint(url="opc.tcp://127.0.0.1:5091")
# opc_server.set_server_name("FreeOpcUa Example Server")

# set all possible endpoint policies for clients to connect through


def get_millisecond_from_date_time(date_time):
    tz = pytz.timezone('Asia/Kolkata')
    dt_with_tz = tz.localize(date_time, is_dst=None)
    seconds = (dt_with_tz - datetime.datetime(1970, 1, 1, tzinfo=pytz.UTC)).total_seconds()
    return seconds * 1000


# print(datetime.timedelta(days=1))


def history_data(state, device_id, start_time=None, end_time=datetime.datetime.now()):
    kairos.set_metrics_name('ilens.live_data.raw')
    kairos.set_metrics_tags({"category_3": device_id})
    # Not working with set_start_end_date function
    # use set_relative instead
    kairos.set_start_end_date(state, start_time, end_time)
    # kairos.set_relative_time(2)

    # kairos.set_metrics_aggregators([
    #     {
    #       "name": "sum",
    #       "sampling": {
    #         "value": "1",
    #         "unit": "milliseconds"
    #       }
    #     }
    #   ])
    # kairos.set_metrics_tags({
    #     "category_3": [
    #       "device_instance_486"
    #     ]
    #   })
    print(json.dumps(kairos.query))

    # response = requests.post(kairosdb_server + "/api/v1/datapoints/query", json.dumps([kairos.query]))
    response = kairos.get_kairos_data()
    print(response)
    # print(response.url)
    # print(response.json())
    data = kairos.get_kairos_data()
    total_data = data[0]['values']
    print(total_data)
    return data

# TODO: This code is not working so, dont touch it..........!!!!!!!!!!!!!!!!!!!
now_ = datetime.datetime.now()  # TODO: check other than relative time
diff = now_ - datetime.timedelta(days=1)
start_time = get_millisecond_from_date_time(diff)
end_time = time.time()
# start_date = get_millisecond_from_date_time(timedelta(days=1))

history_data(False, "device_instance_486", int(start_time), int(end_time))
