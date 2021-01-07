import OpenOPC
import time
import pywintypes
pywintypes.datetime = pywintypes.TimeType
opc_da = OpenOPC.client()

server_list = opc_da.servers()
print(server_list)
opc_da.opc_server('Cogent.DataHub.1', '192.168.5.45')

list_simulator = opc_da.list()
# print(list_simulator)
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


############### Matrikon Server ##################

opc_da.connect('Matrikon.OPC.Simulation.1')
list_simulator = opc_da.list()
print(list_simulator)
simulation_data = opc_da.list(list_simulator[1])
print(simulation_data)
all_tags = opc_da.read(simulation_data)
print(type(all_tags))
# print(all_tags)
# for i in list_simulator:
#     see = opc_da.read(i)
#     print(see)
while True:
   try:
       value = opc_da.read(simulation_data,update=1) # pass tags list here
       print (value)
   except OpenOPC.TimeoutError:
       print ("TimeoutError occured")

   time.sleep(1)