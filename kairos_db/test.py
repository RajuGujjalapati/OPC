from datetime import datetime

import pytz
import pandas as pd

from kairos import Kairos


def get_millisecond_from_date_time(date_time):
    tz = pytz.timezone('Asia/Kolkata')
    dt_with_tz = tz.localize(date_time, is_dst=None)
    seconds = (dt_with_tz - datetime(1970, 1, 1, tzinfo=pytz.UTC)).total_seconds()
    return seconds * 1000


start_date_time = datetime.strptime('27-10-2020 00:00:00', "%d-%m-%Y %H:%M:%S")
end_date_time = datetime.now().strptime('28-10-2020 00:00:00', "%d-%m-%Y %H:%M:%S")
start_millisecond = get_millisecond_from_date_time(start_date_time)
end_millisecond = get_millisecond_from_date_time(end_date_time)

kairos = Kairos()

kairos.set_metrics_tags({"category_3": ['device_instance_371'], "category_5": ['tag_293']})
kairos.set_metrics_name("ilens.live_data.raw")
kairos.set_start_end_date(True, start_millisecond, end_millisecond)
kairos.set_metrics_aggregators([
        {
          "name": "sum",
          "sampling": {
            "value": "1",
            "unit": "milliseconds"
          }
        }
      ])
response = []
try:
    response = kairos.get_kairos_data()

except Exception:
    pass


df = pd.DataFrame(response[0]['values'], columns=["TimeStamp", "values"])

df['TimeStamp'] = pd.to_datetime(df['TimeStamp'], unit='ms').dt.tz_localize('GMT').dt.tz_convert('Asia/Kolkata').dt.tz_localize(None)

print(df['values'])