from opcua import Client
client = Client("opc.tcp://127.0.0.1:49330")
client.connect()
objects = client.get_objects_node()
print(objects)
all_child = objects.get_children()
print(all_child)
simu = objects.get_children()[-1]
print(simu)
node = client.get_node(simu)
print(node)
dev = simu.get_children()
read_tag = dev[-1]
dev_child = read_tag.get_children()
tag_data = dev_child[-1]
print(tag_data.get_value())
print(tag_data.get_data_type())
from opcua import ua
dv = ua.DataValue(ua.Variant(10923, ua.VariantType.Int32))# specify the datatype
#https://python-opcua.readthedocs.io/en/latest/_modules/opcua/ua/uatypes.html
# url is for checking  the datatype accrding to NodeID
dv.ServerTimestamp = None# there was an diff in showing the datatype of an element
dv.SourceTimestamp = None
tag_data.set_value(dv)# success
