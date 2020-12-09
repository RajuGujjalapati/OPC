from opcua import Client
#client = Client("opc.tcp://desktop-tm6jk0c:62640/IntegrationObjects/ServerSimulator")
#client = Client('opc.tcp://raju:boss@desktop-tm6jk0c:62640/IntegrationObjects/ServerSimulator')
client = Client('opc.tcp://localhost:5002')
client.connect()
print("connected")

from datetime import datetime
#strt_time = datetime(2020, 11,27, 9,37,5)
#endtime  = datetime(2020, 11,27, 9,45,5)
tempsensw = client.get_node("ns=2;i=2")
res = tempsensw.read_raw_history()
import pandas as pd
df = pd.DataFrame(res)
df.to_csv('fr.csv')
print(df)
print(res)
# res1 = [i.value for i in res]
# print(res1)
print(len(res))
try:
    from time import sleep
    while True:
        
        tempsensw = client.get_node("ns=2;i=2")#
        print("pass", tempsensw)
        print(tempsensw.get_value())
        #msclt = SubHandler()
        from datetime import datetime
        #strt_time = datetime(2020, 11,27, 9,37,5)
        #endtime  = datetime(2020, 11,27, 9,45,5)
        #sd=tempsensw.read_raw_history(strt_time)
        #print(sd.value)
        #sub = client.create_subscription(100, msclt)
        #handle = sub.subscribe_events(tempsens, tempsensw)
        sleep(1)
except ConnectionResetError:
    client.close_session()
