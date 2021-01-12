import OpenOPC
import time
import pywintypes

pywintypes.datetime = pywintypes.TimeType
opc_da = OpenOPC.client()
print()

server_list = opc_da.servers()
OpenOPC.open_client('192.168.5.45', 135)
print(server_list)
OpenOPC.open_client('192.168.5.45', 4840)
opc_da.connect('Kepware.KEPServerEX.V6')

list_simulator = opc_da.list()
print(list_simulator)
# simulation_data = opc_da.list(list_simulator[0])
# for i in list_simulator:
#     see = opc_da.read(i)
#     print(see)
# while True:
#    try:
#        value = opc_da.read(list_simulator,update=1) # pass tags list here
#        print (value)
#    except OpenOPC.TimeoutError:
#        print ("TimeoutError occured")
#
#    time.sleep(1)


############ Matrikon Server ############

opc_da.connect('Kepware.KEPServerEX.V6')
list_simulator = opc_da.list()
print(list_simulator)
simulation_data = opc_da.list(list_simulator) # 1 for matrikon
print(simulation_data)
all_tags = opc_da.read(simulation_data)
print(type(all_tags))
# print(all_tags)
# for i in list_simulator:
#     see = opc_da.read(i)
#     print(see)
while True:
    try:
        value = opc_da.read(simulation_data, update=1)  # pass tags list here
        print(value)
    except OpenOPC.TimeoutError:
        print("TimeoutError occured")

    time.sleep(1)
