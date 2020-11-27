from opcua import Client
#client = Client("opc.tcp://desktop-tm6jk0c:62640/IntegrationObjects/ServerSimulator")
#client = Client('opc.tcp://raju:boss@desktop-tm6jk0c:62640/IntegrationObjects/ServerSimulator')
client = Client('opc.tcp://localhost:5000')
client.connect()
print("connected")
from time import sleep
########## start with #######
class SubHandler(object):

    """
    Subscription Handler. To receive events from server for a subscription
    data_change and event methods are called directly from receiving thread.
    Do not do expensive, slow or network operation there. Create another
    thread if you need to do such a thing
    """
    def event_notification(self, event):
        print("New event recived: ", event)
ns = client.get_namespace_array()
print(ns)
root = client.get_root_node()
print(root)
objects = client.get_objects_node()
print(objects)
tempsens = objects.get_children()
print(tempsens)
print(tempsens[1].get_children())
#print("Objects node is: ", root)
try:
    while True:
        tempsensw = client.get_node("ns=2;i=1")#
        print("pass", tempsensw)
        print(tempsensw.get_value())
        msclt = SubHandler()
        sub = client.create_subscription(100, msclt)
        handle = sub.subscribe_events(tempsens, tempsensw)
        sleep(1)
except ConnectionResetError:
    client.close_session()


#print(client.get_namespace_array())
#objects = client.get_objects_node()
#print(objects)
#print("..............",objects.get_children())#  node seperation --> a[0].split('(')[2].split(')')[0]
#tempsens = objects.get_children()[1].get_browse_name()
#print(tempsens)
#print(objects.get_child(tempsens)) # we can get values by using qualified name also...
#rs = objects.get_children()[1]
#print(rs.get_value())
#new_var  = objects.get_children()[0].get_browse_name()
#print(objects.get_child(new_var))
"""
from opcua import Client
client = Client("opc.tcp://desktop-tm6jk0c:62640/IntegrationObjects/ServerSimulator:4840")
#client = Client('opc.tcp://192.168.43.110:5000')
client.connect()
var  = client.get_node("ns=2;i=2")
var1 = client.get_node("ns=2;i=3")
print("Initial Value",var.get_value())
print(var1.get_value())
root = client.get_root_node()
objects = client.get_objects_node()
tempsens = objects.get_children()[1].get_browse_name()
print(tempsens)
print("Objects node is: ", root)

# Now getting a variable node using its browse path
obj = objects.get_child('2:Parameters')#error if we are asking to get_child from root node.
print("MyObject is: ", obj)
var.set_value(10000)
print(client.get_namespace_array())
objects = client.get_objects_node()
print(objects)
print("..............",objects.get_children())
tempsens = objects.get_children()[1].get_browse_name()
print(tempsens)
#res = tempsens.get_value()
#print(res)
#bulb = objects.get_children()
#bulb.get_children()

#state = bulb.get_children()[0]
#state.get_value()

#state.set_value(True)
#client.close_session()
"""
