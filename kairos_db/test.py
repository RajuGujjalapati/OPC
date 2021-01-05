from datetime import datetime
from collections import  defaultdict
import pytz
import pandas as pd

from kairos import Kairos
# TODO: This code is working, so use it!!!!!!!!!!!!:)

def get_millisecond_from_date_time(date_time):
    tz = pytz.timezone('Asia/Kolkata')
    dt_with_tz = tz.localize(date_time, is_dst=None)
    seconds = (dt_with_tz - datetime(1970, 1, 1, tzinfo=pytz.UTC)).total_seconds()
    return seconds * 1000


start_date_time = datetime.strptime('28-12-2020 18:34:00', "%d-%m-%Y %H:%M:%S")
end_date_time = datetime.now().strptime('29-12-2020 11:30:00', "%d-%m-%Y %H:%M:%S")
start_millisecond = get_millisecond_from_date_time(start_date_time)
end_millisecond = get_millisecond_from_date_time(end_date_time)

kairos = Kairos()

kairos.set_metrics_tags({"category_3": ['device_instance_486']})
kairos.set_metrics_name("ilens.live_data.raw")
kairos.set_start_end_date(True, start_millisecond, end_millisecond)
# kairos.set_metrics_aggregators([
#         {
#           "name": "sum",
#           "sampling": {
#             "value": "1",
#             "unit": "milliseconds"
#           }
#         }
#       ])
response = []
def test():
    data = response
try:
    response = kairos.get_kairos_data()

except Exception:
    pass
# se = response['values']
print(response)
kairos_dict = defaultdict(dict)

df = pd.DataFrame(response)
df = df.drop(['name','group_by'],axis=1)
final_data = pd.DataFrame()
final_data['tag'] = df['tags'].apply(lambda x: x.get('category_5')[0])
final_data['device'] = df['tags'].apply(lambda x: x.get('category_3')[0])

def seperate(x):
    time = []
    value = []
    for i in x:
        time.append(i[0])
        value.append(i[1])
    return time,value

df2=df['values'][0][0]
# final_data[['time','value']] = df['values'].apply(seperate)
df_s = pd.DataFrame(df['values'])
print(df_s)
# df['TimeStamp'] = pd.to_datetime(df['TimeStamp'], unit='ms').dt.tz_localize('GMT').dt.tz_convert('Asia/Kolkata').dt.tz_localize(None)

print(df)