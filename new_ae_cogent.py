import traceback
import time
from opcua import Client
from datetime import datetime

# import requests
# res = requests.get("http://admin:admin@elmpc-129:51311/CogentDataHub/DataAccess")
# tes = res.text()
from opcua.ua import UaError


class SubHandler(object):
    """
    Subscription Handler. To receive events from server for a subscription
    """
    '''def data_change(self, handle, node, val, attr):
        print("Python: New data change event", handle, node, val, attr)

    def event(self, handle, event):
        print("Python: New event", handle, event)'''

    def datachange_notification(self, node, val, data):
        print("Python: New data change event", node, val)

    def event_notification(self, event):
        print("Python: New event", event.EventType)


try:
    client = Client("opc.tcp://raju:qwertyuiopasdf@DESKTOP-TM6JK0C:5002")
    # print(client.get_endpoints())
    # http://elmpc-129:51311/CogentDataHub/DataAccess

    # client = Client("http://admin:admin@elmpc-129:51311/CogentDataHub/DataAccess")
    conn = client.connect()
    print(client.get_endpoints())
    print(client.find_servers())
except ConnectionRefusedError:
    traceback.print_exc()
    print("Error in Connecting to the server, Check the Host & Port")

objects = client.get_objects_node()
# get_browse_name()# getting  objects id
print(objects.get_browse_name())
all_child = objects.get_children()
print(all_child)
print([child.get_children() for child in all_child])
he = all_child[3].get_children()
print(he)
for i in he:
    print(client.get_node(i).get_data_value())
myvar = client.get_node("")
handler1 = SubHandler()
sub = client.create_subscription(500, handler1)
print("PDC_MAIN-I-MAIN, Subscription created")
print("////////////////////////////////////////////////////////////////")
# handle = sub.subscribe_data_change(myvar)
# # Subscribe to events from the OPC-UA Server
# eventhandle1 = sub.subscribe_events()
