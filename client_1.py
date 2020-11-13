from opcua import Client
client = Client("opc.tcp://10.0.0.11:4840")
#client = Client('opc.tcp:127.0.0.1:32402')
client.connect()
var  = client.get_node("ns=2;i=2")
print("Initial Value",var.get_value())
var.set_value(10000)
print(client.get_namespace_array())
objects = client.get_objects_node()
print(objects)
print("..............",objects.get_children())
tempsens = objects.get_children()[1]
print(tempsens)
print(client.get_values([85]))
#bulb = objects.get_children()
#bulb.get_children()

#state = bulb.get_children()[0]
#state.get_value()

#state.set_value(True)
client.close_session()
