from opcua import Client
import time
client = Client("opc.tcp://127.0.0.1:5091")
client.connect()

root_node  = client.get_objects_node()
print(root_node.get_browse_name())
tes_chil = root_node.get_children()[1:]
print(tes_chil)
tes = [i for i in tes_chil]
for j in tes_chil:
    # print(j.get_children()[1].get_value())
    while True:
        chil = [(res.get_value(), res.get_browse_name()) for res in j.get_children()]
        print(chil)
        time.sleep(60)

print([i.get_browse_name() for i in tes_chil])