import traceback
import time
from opcua import Client
from datetime import datetime

# import requests
# res = requests.get("http://admin:admin@elmpc-129:51311/CogentDataHub/DataAccess")
# tes = res.text()
try:
    client = Client("opc.tcp://admin:admin@elmpc-129:51310/CogentDataHub/DataAccess")
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
# getting children under registered under the objects
print(all_child)
see_b_name_all_child = []
get_data_child = []
for i in all_child:
    print("*" * 30)
    see_b_name = client.get_node(str(i))  # get all nodes
    print(see_b_name)
    print(see_b_name.get_browse_name())  # getting qualified names
    print(see_b_name.get_children())
    # see_b_name_all_child.append(see_b_name)
    print("*" * 20)
    all_data =[]

    if len(see_b_name.get_children())<1:
        pass
    else:
        print(see_b_name.get_children())
        get_data_child.append(see_b_name.get_children())

print(get_data_child)
while True:
    # for i in get_data_child:
    dictionary=[]
    for data in get_data_child[0]:  # see_b_name.get_children()
        print(data.get_browse_name())
        try:
            dictionary = {str((client.get_node(data).get_browse_name(), datetime.now())): client.get_node(data).get_value()}
        except:
            pass
        finally:
            all_data.append(dictionary)
    print(all_data)
all_childre = [j.get_children() for j in see_b_name_all_child]
# for res in all_childre[0]:
#     try:
#         print(client.get_node(res).get_value())
#     except:
#         pass

    # try:
    #     while True:
    #         all_data = []
    #         for data in see_b_name:  # see_b_name.get_children()
    #             try:
    #                 dictionary = {str((client.get_node(data).get_browse_name(), datetime.now())): client.get_node(data).get_value()}
    #                 all_data.append(dictionary)
    #                 print(all_data)
    #             # print(datetime.now(),":  ",client.get_node(data).get_value())
    #             except:
    #
    #                 pass
    #
    # except:
    #     pass
