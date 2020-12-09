from opcua import Client
try:
    client = Client("opc.tcp://127.0.0.1:5002")
    conn = client.connect()
except ConnectionRefusedError:
    print("Error in Connecting to the server, Check the Host & Port")
print(conn)
objects = client.get_objects_node()# getting  objects id
print(objects)
all_child = objects.get_children()# getting children under registered under the objects
print(all_child)
simu = objects.get_children()[-1]
print(simu)
node = client.get_node(simu)
print(node)
dev = simu.get_children()
read_tag = dev[-1]# selecting the req child
dev_child = read_tag.get_children()
tag_data = dev_child[-1]
print(tag_data.get_value())
print(tag_data.get_data_type())
from opcua import ua
dv = ua.DataValue(ua.Variant(10923, ua.VariantType.Float))# specify the datatype
#https://python-opcua.readthedocs.io/en/latest/_modules/opcua/ua/uatypes.html
# url is for checking  the datatype accrding to NodeID
dv.ServerTimestamp = None #if there is any diff in showing the datatype of an element, try to stop server for sometime and run server again.
dv.SourceTimestamp = None
tag_data.set_value(dv)# success
print(tag_data.get_value())
print(simu.get_children(refs=33))# HierarchicalReferences = 33
last_sec = objects.get_children()[-2]
print(last_sec.get_children(refs=33)[-1].get_children()[-1].get_value())# checkout this for how refs work (https://python-opcua.readthedocs.io/en/latest/_modules/opcua/common/node.html)
print(simu.get_path())
