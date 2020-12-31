import time
from datetime import datetime

import pytz
import pandas as pd
from opcua import ua, Server

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

print(df['values'][0])

if __name__ == "__main__":
    # logging.basicConfig(level=logging.WARN)
    # logger = logging.getLogger("opcua.server.internal_subscription")
    # logger.setLevel(logging.DEBUG)

    # setup our server
    server = Server()
    server.set_endpoint("opc.tcp://192.168.6.162:5010")
    # setup our own namespace, not really necessary but should as spec
    uri = "TEst"
    idx = server.register_namespace(uri)
    print("idx", idx)
    # get Objects node, this is where we should put our custom stuff
    objects = server.get_objects_node()
    print("objects", objects)
    # populating our address space
    myobj = objects.add_object(idx, "MyObject")
    print("myobj", myobj)
    myprop = myobj.add_property(idx, "MyProperty", 21) # for testing purpose....
    myvar = myobj.add_variable(idx, "MyVariable", ua.Variant(0.25, ua.VariantType.Double))
    print(myvar)
    myfl = myobj.add_variable(idx, "FLoat", ua.Variant(20.7, ua.VariantType.Float))
    myprop.set_writable()
    myfl.set_writable()
    myvar.set_writable()
    # Creating a custom event: Approach 1
    # The custom event object automatically will have members from its parent (BaseEventType)
    etype = server.create_custom_event_type(idx, 'MyFirstEvent', ua.ObjectIds.BaseEventType,
                                            [('MyNumericProperty', ua.VariantType.Float),
                                             ('MyStringProperty', ua.VariantType.Double)])
    print(etype)
    myevgen = server.get_event_generator(etype, myobj)

    # Creating a custom event: Approach 2
    custom_etype = server.nodes.base_event_type.add_object_type(2, 'MySecondEvent')
    custom_etype.add_property(2, 'MyIntProperty', ua.Variant(22, ua.VariantType.Int32))
    custom_etype.add_property(2, 'MyBoolProperty', ua.Variant(True, ua.VariantType.Boolean))
    mysecondevgen = server.get_event_generator(custom_etype, myobj)
    #############Testing
    custom_etype1 = server.nodes.base_event_type.add_object_type(3, 'MySecondEvent3')

    custom_etype1.add_property(2, 'MyIntProperty11', ua.Variant(67, ua.VariantType.Int32))
    custom_etype1.add_property(2, 'MyBoolProperty11', ua.Variant(False, ua.VariantType.Boolean))
    mysecondevgen1 = server.get_event_generator(custom_etype1, myobj)
    df_le = len(df)
    print(df_le)
    count=0
    server.start()
    while df_le>0:
        choices = [True, False]
        # myvar.set_value()
        myfl.set_value(df['values'][count])
        print(myfl.get_value())
        # myprop.set_value(random.randrange(1, 800))
        df_le-=1
        count+=1
        time.sleep(5)
