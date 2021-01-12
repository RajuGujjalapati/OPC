from opcua import Client

client = Client("opc.tcp://localhost:5345/four_tank_process/")

client.connect()

obj = client.get_objects_node()
print(obj.get_children())
main_chil = obj.get_children()[1:]
for i in main_chil:
    print(client.get_values(i.get_children()))
    all_child = i.get_children()
    for k in all_child:
        print(k.get_browse_name())
    print(i.get_browse_name())
