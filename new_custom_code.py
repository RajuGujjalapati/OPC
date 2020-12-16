import traceback
from opcua import Client

client = Client("opc.tcp://admin:admin@elmpc-129:51310/CogentDataHub/DataAccess")
client.connect()
all_ob = client.get_objects_node()

#
# def check(node_data):
#     if isinstance(node_data, list):
#         res = list_handler(node_data)
#         return res
#     else:
#         res = node_data.get_children()
#         if isinstance(node_data, list):
#             res = list_handler(node_data)
#             return res
#         return res
#
# def list_handler(node_ids):
#     store_objs = []
#     for data_points in node_ids:
#         try:
#             child = data_points.get_children()
#             if isinstance(child, list):
#                 return list_handler(child)
#
#         except Exception as e:
#             # traceback.print_exc()
#             # check(node_ids)
#             data = client.get_node(data_points).get_value()
#             store_objs.append(data)
#             return capture_data(data)
#
#
# def capture_data(data, total=[]):
#     total.append(data)
#     return data
# print(all_ob)
# print(all_ob.get_children())
# stat = check(all_ob.get_children()[1:])
# print(type(stat))
# print(capture_data(list_handler(check(stat))))
from opcua.ua.uaerrors import BadAggregateInvalidInputs, BadAttributeIdInvalid
store_all_list_node=[]
def get_all_data_values(node):
    try:
        data = client.get_node(str(node))
        store_all_list_node.append(data)
        data = data.get_value()
        # print(data)
        """Here we are getting values from the server, what we need to check is whether the request is first or not if the request is first do the
        process like we did.
        But if the request is second or more then at first request we are going to store the neccessary(which are giving data) nodes
        and then after first request we are going to call that stored nodes."""
    except BadAggregateInvalidInputs:
        if isinstance(node, list):
            main_(node)
        main_(node)
        traceback.print_tb()
        pass

    return data


def main_(data):
    try:
        get_all_data_values(data)
    except BadAttributeIdInvalid:
        check_child = data.get_children()
        if isinstance(check_child, list):
            for some_data in check_child:
                try:
                    get_all_data_values(some_data)
                except BadAttributeIdInvalid:
                    pass

        else:
            traceback.print_exception()
print(all_ob.get_children_descriptions())
print('#'*20,all_ob.get_children(refs=33))
print(client.load_type_definitions())
# print(client.load_enums())
one = all_ob.get_children(refs=33)
for i in one:
    two = i.get_children(refs=33)
    print(two)
list_of_nodes = all_ob.get_children()[1:]
for i in list_of_nodes:
    # print(i.get_children())
    if i:
        main_(i)
        print(store_all_list_node)
while True:
    for ch in store_all_list_node:
        print()
        try:
            print(ch.get_value())
            print(ch.get_browse_name())

        except BadAttributeIdInvalid:
            main_(ch)

