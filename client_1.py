from opcua import Client
client = Client("opc.tcp://desktop-tm6jk0c:62640/IntegrationObjects/ServerSimulator")
#client = Client('opc.tcp://192.168.43.110:5000')
root = client.get_root_node()
print(root)
objects = client.get_objects_node()
print(objects)
#tempsens = objects.get_children()
#print(tempsens)
#print("Objects node is: ", root)

print(client.get_namespace_array())
objects = client.get_objects_node()
print(objects)
print("..............",objects.get_children())
tempsens = objects.get_children()[1].get_browse_name()
print(tempsens)





























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
