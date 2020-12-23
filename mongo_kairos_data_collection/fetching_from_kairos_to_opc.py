from kairos import Kairos
import pytz
import datetime
import pandas as pd
from opcua import Server
from mongo_query import live_data_collection
from datetime import timedelta
import time, requests
import json

kairosdb_server = "http://192.168.4.95:18085"
opc_server = Server()
opc_server.set_endpoint(url="opc.tcp://127.0.0.1:5091")
opc_server.set_server_name("FreeOpcUa Example Server")

# set all possible endpoint policies for clients to connect through

# setup our own namespace
uri = "http://examples.freeopcua.github.io"
idx = opc_server.register_namespace(uri)


def get_millisecond_from_date_time(date_time):
    tz = pytz.timezone('Asia/Kolkata')
    dt_with_tz = tz.localize(date_time, is_dst=None)
    seconds = (dt_with_tz - datetime.datetime(1970, 1, 1, tzinfo=pytz.UTC)).total_seconds()
    return seconds * 1000


now_ = datetime.datetime.now()
diff = now_ - datetime.timedelta(minutes=1)
# print(diff)
# start_date_time = datetime.strptime('1-12-2020 1:00:00', "%d-%m-%Y %H:%M:%S")
start_date_time = get_millisecond_from_date_time(diff)
end_millisecond = time.time()
# start_millisecond = get_millisecond_from_date_time(start_date_time)
# end_millisecond = get_millisecond_from_date_time(diff)

data = live_data_collection()
print(data)
kairos = Kairos()
kairos.set_relative_time(start_time=5, unit='minutes')
opc_server.start()


def final_data_for_opc():
    for col_name, row_data in data.iterrows():
        device = row_data.category_3
        print(device)
        dev_list = []
        dev = opc_server.nodes.objects.add_object(idx, str(row_data.category_3))
        if dev in dev_list:
            pass
        dev_list.append(dev)
        """
        all_tags = [row for row, val in row_data.value.items()]
        all_tags_data = [val for row, val in row_data.value.items()]
        print(all_tags)
        print(all_tags_data)
        """

        for row, val in row_data.value.items():
            kairos.set_metrics_name('ilens.live_data.raw')
            kairos.set_metrics_tags({"category_3": [str(row_data.category_3)], "category_5": [str(row)]})
            # kairos.set_metrics_aggregators([
            #     {
            #         "name": "sum",
            #         "sampling": {
            #             "value": "1",
            #             "unit": "milliseconds"
            #         }
            #     }
            # ])
            # kairos.set_start_end_date(True, start_date_time, end_millisecond)
            # kairos.set_relative_time(start_time=5, unit='minutes')
            response = requests.post(kairosdb_server + "/api/v1/datapoints", json.dumps([kairos.query]))
            # print(response.data)
            # print("Simple test [without compression]: \t%d (status code)" % response.status_code )
            # print(kairos.query)
            res = kairos.get_kairos_data()
            total_data = res[0]['values']  # final data stops at 02-12-2020;
            if total_data == []:
                continue
            print(total_data)

            tag_list = []
            if str(dev) in dev_list:
                tag = dev.add_variable(idx, str(row))
                tag.set_writable()



            # total_data[0].extend((str(row), str(row_data.category_3)))
            # print(total_data)
            tag = dev.add_variable(idx, str(row), val)
            tag.set_writable()
    return
            
            # return total_data
            # df = pd.DataFrame(res[0]['values'], columns=["TimeStamp", "values"])
            # print(df)
        # print(res)


# def opc_server_handler():
    # data = final_data_for_opc()
    # # dev_list = []
    # # dev_list.append(str(data[0][3]))
    # # if str(data[0][3]) in dev_list:
    # #     pass
    # dev = opc_server.nodes.objects.add_object(idx, str(data[0][3]))
    # # dev_list.append(str(dev))
    # tag_data = []
    # tag_data.append(data[0][2])
    # # if data[0][2] in tag_data:
    # #     tag = dev.add_variable(idx, str(data[0][2]), data[0][1])
    # tag = dev.add_variable(idx, str(data[0][2]), data[0][1])
    # tag.set_writable()
    # return
import time
proce = 0
if __name__ == '__main__':
    while True:
        if proce == 0:
            final_data_for_opc()
            proce+=1
        time.sleep(60)
        raise Exception("WE ARE IN SLEEP MODE")
        final_data_for_opc()

