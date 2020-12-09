from datetime import datetime, timedelta
from kairos import Kairos
import pytz

def get_millisecond_from_date_time(date_time):
    tz = pytz.timezone('Asia/Kolkata')
    dt_with_tz = tz.localize(date_time, is_dst=None)
    seconds = (dt_with_tz - datetime(1970, 1, 1, tzinfo=pytz.UTC)).total_seconds()
    return seconds * 1000


start_date_time = datetime.strptime("01-01-2020 00:00:00", "%d-%m-%Y %H:%M:%S")
end = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
end_date_time = datetime(year=int(end.split(' ')[0].split('-')[0]), month=int(end.split(' ')[0].split('-')[1]),
                            day=int(end.split(' ')[0].split('-')[2]))

start_millisecond = get_millisecond_from_date_time(start_date_time)
end_millisecond = get_millisecond_from_date_time(end_date_time)

kairos = Kairos()

from opcua import Client
# client = Client("opc.tcp://10.0.0.11:4840")
client = Client('opc.tcp://com_sam:Elmeasure@192.168.5.254:4840/test')
client.connect()
def insert_data(value, tag): #100081
    current_time = get_millisecond_from_date_time(datetime.now().replace(second=00, microsecond=00))

    date_points = [current_time, value]
    print(date_points)

    pridction = [{"name": "ilens.live_data.raw", "datapoints": date_points, 'tags': {"category_3": "device_instance_188", "category_5": tag,
                                "category_1": "industry_3_client_1107", "category_2": "gateway_instance_2"}} ]
    
    kairos.set_update_query_name("ilens.live_data.raw")
    kairos.set_update_query_datapoints(date_points)
    kairos.set_update_query_tags({"category_3": "device_instance_188", "category_5": tag})
    kairos.update_kairos_data()
    # kairos.set_start_end_date(True, start_millisecond, end_millisecond)
    # response = kairos.get_kairos_data()
    # print(response)
while True:
    try:
        var  = client.get_node("ns=2;i=2")
        var1 = client.get_node("ns=2;i=3")
        var_res = var.get_value()
        insert_data( var_res, tag='tag_100081')
        print("Initial Value",var.get_value())
        var1_res = var1.get_value()
        insert_data( var1_res, tag='tag_100082')
        
        import time
        time.sleep(1)
    except (TypeError, ConnectionError):
        print("we are in Exception ")
        pass

# var.set_value(10000)
'''for insert uncomment change category and tag'''

# kairos.set_metrics_tags({"category_3": "device_instance_188", "category_5": "tag_293",
#                          "category_1": "industry_3_client_1107", "category_2": "gateway_instance_2"})
# kairos.set_metrics_name("ilens.live_data.raw")
# kairos.set_start_end_date(True, start_millisecond, end_millisecond)
#
# kairos.set_metrics_aggregators([
#     {
#         "name": "filter",
#         "filter_op": "lte",
#         "threshold": "0"
#     },
#     {
#         "name": "first",
#         "sampling": {"value": "15", "unit": 'minutes'},
#         "align_start_time": True
#     },
#     {
#         "name": "diff"
#     },
#     {
#         "name": "filter",
#         "filter_op": "lte",
#         "threshold": "0"
#     }
# ])
#
# response = []
# try:
#     response = kairos.get_kairos_data()
#
# except Exception:
#     pass

''' insertion'''


