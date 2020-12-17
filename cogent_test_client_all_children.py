import traceback
import time
from opcua import Client
from datetime import datetime

# import requests
# res = requests.get("http://admin:admin@elmpc-129:51311/CogentDataHub/DataAccess")
# tes = res.text()
from opcua.ua import UaError

try:
    client = Client("opc.tcp://elmpc-129:51310/CogentDataHub/DataAccess/AE")
    # print(client.get_endpoints())
    # http://elmpc-129:51311/CogentDataHub/DataAccess

    client = Client("http://admin:admin@elmpc-129:51311/CogentDataHub/DataAccess")
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


def type_list(node):
    for _ in node:
        return getting_chidren(_)


def is_null(node, allnode=[]):
    return allnode.append(node)


def not_null(node):
    pass


def getting_chidren(nodeid):
    child = nodeid.get_children()
    if nodeid == []:
        is_null(nodeid)
    if type(nodeid) == list:
        all_nodes = type_list(nodeid)

    if len(child) == 0:
        is_null(child)
    print("......................................",child)
    return child



def incoming_nodes(node):
    if  (type(node) == list):
        all_childrens(node)
    else:
        setuu.extend(node)
setuu = []


def all_childrens(node):
    if  len(str(node))==0:
        setuu.extend(node)
    if type(node)==list:
        try:
            for _ in node:
                nodes = _.get_children()
                return incoming_nodes(nodes)
        except TypeError:
            nodes = node.get_children()
            return incoming_nodes(nodes)

    else:
        return incoming_nodes(node.get_children())

for i in all_child[1:]:
    all_childrens(i)
    print(setuu)
# def getting_value():
#     pass
#
#
# def getting_chidrens(i):
#     pass



# child_children = [i.get_children() for i in all_child[1:]]
# print(child_children[0])
# final_node = []
# for _ in child_children:
#     final_node.extend(_)
# print(final_node)
# daat_child = []
# for _ in final_node:
#     sdk = _.get_children()
#     if len(sdk)< 1:
#         daat_child.append(_)
#     sdf = [_.get_children() for _ in sdk]
#     daat_child.extend((sdk, sdf))

# try:
#     sdk = _.get_children()
#     daat_child.append(sdk)
# except Exception as e:
#     traceback.format_exc()
#     daat_child.append(_)

# print(daat_child)
# while 1:
#     res = []
#     for data in daat_child:
#         try:
#             ch = {str(client.get_node(data).get_browse_name()): client.get_node(data).get_value()}
#             # print(ch)
#             res.append(ch)
#
#         except UaError:
#
#             traceback.print_exc()
#             pass
#     print(res)
