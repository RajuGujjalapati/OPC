import traceback

from opcua import Client
conne = False
client = Client("opc.tcp://com.tom:Elmeasure@192.168.4.181:4840/test")
# client.set_security()
client.application_uri = "urn:com-tom:OpcUaServer"


client.set_security_string(r"Basic256Sha256,SignAndEncrypt,"
                           r"C:\Users\New\OneDrive\Desktop\El_Measure\test_sessionOpenssl\clean\comtom\cert.der,"
                           r"C:\Users\New\OneDrive\Desktop\El_Measure\test_sessionOpenssl\clean\comtom\key.pem")
try:
    client.connect()
    conne = True
    obj = client.get_objects_node()
    obj_bn = client.get_objects_node().get_browse_name()
    print(obj_bn)
    print(obj)
    dri = obj.get_children()  ##out2
    print(dri)
    for i in dri:
        print("*" * 30)
        see_b_name = client.get_node(str(i))  # get all nodes
        print(see_b_name)
        print(see_b_name.get_browse_name())  # getting qualified names
        print(see_b_name.get_children())
        print("*" * 20)
    node = client.get_node("ns=1;i=4")  # get_qualified_name/browsename single node
    print(node)
    data = node.get_children()
    print(data)
    # for i in data:
    tes = [_.get_children() for _ in data]  # Earlier, here we have used data[0].get_children()
    print(tes)
    import time

    while conne:
        for j in tes:  # list of list
            # print(j[0].get_browse_name())
            for i in j:  # parsing lists
                # print(j)
               # print(client.get_node(i).get_browse_name())  # for getting the browse name don't give str(i), use that only for get_value()
                out1 = client.get_node\
                    (str(i)).get_value()  # getting the nodes
                print(len(out1))
                print(out1)
            time.sleep(0.5)

    # print(node.get_value())
except Exception as e:
    traceback.print_exc()
    client.disconnect()
    client.close_session()
    conne = False
# finally:
#     client.disconnect()
