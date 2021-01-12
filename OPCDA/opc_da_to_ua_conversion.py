# Name: opcda_to_opcua.py
# Author: Eskild Schroll-Fleischer <esksch@dtu.dk>
# Date: 30th of August 2017
#
# Description:
# Proxy between OPC-DA server and OPC-UA client.
# Firstly the OPC-DA namespace is traversed using a recursive
# function. These variables are then classified as readable or writable
# and added to the OPC-UA namespace. The readable variables are read
# periodically from the OPC-DA server and published on the OPC-UA server.
# The writable OPC-UA tags are monitored for changes. When a change is
# caught then the new value is published to the OPC-DA server.
#
# The code is organized as follows:
# 1. Configuration
# 2. Connec to OPC-DA server
# 3. Discover OPC-DA server nodes
# 4. Subscribe to datachanges coming from OPC-UA clients
# 5. Read all readables simultaneously and update the OPC-UA variables
#    to reflect the OPC-DA readings

# Requires Anaconda, OpenOPC
# L 609 in address_space.py, python-opcua v 0.90.3
import pywintypes
import logging, time, sys, decimal, OpenOPC
from datetime import datetime
from opcua import ua, uamethod, Server

## 1. Configuration
OPC_DA_SERVER = ''#Matrikon.OPC.Simulation.1
# OPC_UA_CERTIFICATE = 'certificate.der'
# OPC_UA_PRIVATE_KEY = 'private_key.pem'
OPC_UA_URI = 'http://dtu.dk'

# Constants
ITEM_ID_VIRTUAL_PROPERTY = 0
ITEM_CANONICAL_DATATYPE = 1
ITEM_VALUE = 2
ITEM_QUALITY = 3
ITEM_TIMESTAMP = 4
ITEM_ACCESS_RIGHTS = 5
SERVER_SCAN_RATE = 6
ITEM_EU_TYPE = 7
ITEM_EU_INFO = 8
ITEM_DESCRIPTION = 101
ACCESS_READ = 0
ACCESS_WRITE = 1
ACCESS_READ_WRITE = 2
pywintypes.datetime = pywintypes.TimeType
# Set up server
server = Server()
server.set_endpoint('opc.tcp://localhost:5345/four_tank_process/')
# server.load_certificate(OPC_UA_CERTIFICATE)
# server.load_private_key(OPC_UA_PRIVATE_KEY)
uri = OPC_UA_URI
idx = server.register_namespace(uri)
root = server.nodes.objects.add_object(idx, OPC_DA_SERVER)
print(root)
## 2. Connect to OPC-DA server
c = OpenOPC.client()
objects = server.get_objects_node()

process = 1


class StartServer:
    def __init__(self, url):
        self.url = url
        self.process = 1
        self.opc_da = OpenOPC.client()
        self.client = self.opc_da.connect(url)
        print(self.client)

    def folder_creation(self):
        data = self.opc_da.list()
        print(data)
        if isinstance(data, list):
            folder_names = [objects.add_folder(idx, i) for i in data]
            print(folder_names)
        return data

    def dynamic_tag_generator(self):

        folder_data = StartServer.folder_creation(self)
        print(";;;;;;;;;;;;", folder_data)
        tags = self.opc_da.list(folder_data)
        print(tags)
        if isinstance(tags, list):
            value = self.opc_da.read(tags, update=-1)
            print(value)

            global tag_names_values
            all_tags = []
            print("process", self.process)
            if self.process == 1:
                tag_names_values = [objects.add_variable(idx, i, 0) for i, j in zip(tags, value)]
                print(tag_names_values)
                all_tags.append(tags)
                making_witable = [_.set_writable() for _ in tag_names_values]
                print(making_witable)
                self.process += 1
                print("process", self.process)
            else:
                print(100 * '&')
                while True:
                    # updating = [i.set_value(j[1]) for i, j in zip(tags, value)]
                    chec = [0 if j[1] is None else int(j[1]) for i, j in zip(tags, value)]
                    print(chec)
                    updating = [i.set_value(0) if j[1] is None else i.set_value(j[1]) for i, j in
                                zip(tag_names_values, value)]
                    print(updating, "sleeping")
                    time.sleep(2)


server.start()
my_server = StartServer("Matrikon.OPC.Simulation.1")
folder_data = my_server.folder_creation()
for i in range(200):
    print("see", my_server.dynamic_tag_generator())

# List OPC-DA servers
servers = c.servers()
c.connect(OPC_DA_SERVER)
def after_conn():
    res = c.connect(OPC_DA_SERVER)
    print(res)
    conn = True
    print(".....................................", c.list())
    first_list = c.list()

    all_tags = c.list(first_list)
    print(all_tags)
    lst = c.list(all_tags)
    print(",,,,,,,,,,,,,,,,,,,,,,,,,,,", lst)
    return all_tags


def tag_data_check():
    # this function will check recursively to get final tags
    pass


all_tags_names = after_conn()

# while True:
#     value = c.read(all_tags_names, update=200)  # pass tags list here
#     value = [(i[1] == 0, i[0]) if i[1] is None else (i[0], int(i[1])) for i in value]
#     print(value)


class SubscriptionHandler(object):
    def __init__(self, n):
        self.i = 0
        self.n = n

    def final_datachange_notification(self, node, val, data):
        path_as_string = node.get_path_as_string()
        # 'path_as_string' is a list of strings containing:
        # 0: 0:Root
        # 1: 1:Objects
        # 2: 2:OPC DA Server
        # 3 and onwards: 3:[Step of path to node in OPC-DA]
        opc_da_address = '.'.join([a.split(':')[1] for a in path_as_string[3:]])
        cc = OpenOPC.client()
        cc.connect(OPC_DA_SERVER)
        print('Datachange', opc_da_address, val, cc.write((opc_da_address, val,)))
        cc.close()

    # This function is called initially to catch the notifications from newly added nodes
    def datachange_notification(self, node, val, data):
        self.i = self.i + 1
        # print('Catching meaningless datachange notification')
        if self.i == self.n:
            # print('Finished catching meaningless datachange notifications')
            self.datachange_notification = self.final_datachange_notification


def read_value(value):
    value = value[0]
    if isinstance(value, decimal.Decimal):
        value = float(value)
    elif isinstance(value, list):
        if len(value) == 0:
            value = None
    elif isinstance(value, tuple):
        if len(value) == 0:
            value = None
    return value


def live_data_tracker_da_server():
    pass


readable_variable_handles = {}
writeable_variable_handles = {}
# nodes = c.list('*', recursive=True) # use this to get every node in the server.............
nodes = c.list()
print(nodes)
# 'nodes' is a list of dot-delimited strings.
tree = {}
for node in nodes:
    parts = node.split('.')
    print(parts)
    # Folders are the steps on the path to the file.
    folders = parts[:-1]
    print(folders)
    file = parts[-1]
    print(file)
# Create folder tree if it does not already exist-
# tree[path] = parent.add_folder(idx, folder)
# opcua_node = tree[path].add_variable(idx, file, ua.Variant(current_value, ua.VariantType.UInt16))
try:
    server.start()
    ## 4. Subscribe to datachanges coming from OPC-UA clients
    handler = SubscriptionHandler(len(writeable_variable_handles))
    sub = server.create_subscription(100, handler).subscribe_data_change(writeable_variable_handles.values())
    readables = list(readable_variable_handles.keys())
    while True:
        time.sleep(0.5)
        ## 5. Read all readables simultaneously and update the OPC-UA variables
        for reading in c.read(readables):
            opc_da_id = reading[0]
            variable_handle = readable_variable_handles[opc_da_id]
            variable_handle.set_value(read_value(reading[1:]))
finally:
    pass
    # server.stop()
    # c.close()
