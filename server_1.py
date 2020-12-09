import math
from opcua import Server, ua
from random import randint
from time import sleep
server = Server()
server.set_endpoint("opc.tcp://127.0.0.1:8080")
add_space = server.register_namespace("RooM1")
node = server.get_objects_node()
#print(node.get_attributes())########################################
param = node.add_object(add_space, "Parameters") # this may be optional, it creates a folder structure.
print(param)

#Temp = param.add_variable(add_space, "Temperature", 0)# sensor # (nodeid, bname, val, varianttype=None, datatype=None)


Temp = param.add_variable(add_space, "MyVariable", ua.Variant(0, ua.VariantType.Double))# type of variable
Press = param.add_variable(add_space, "Pressure", ua.Variant(0, ua.VariantType.Double))
print(Temp)
print(Press)
Temp.set_writable()
Press.set_writable()
# adding new object for nodes, below is the diff ways, to add varibale to node
tempsens = Temp.add_object('ns=2;s="TS1"',"Tempearature Sensor 1") # parent node-id
tempsens.add_variable('ns=2;s="TS1_VendorName"',"TS1 Vendor Name", "Sensore King")
tempsens.add_variable('ns=2;s="TS1_SerialNumber"',"TS1 Serial Name", 12345678)
#temp = tempsens.add_variable('ns=2;s="TS1_Temperature"', "TS1 Temperature", 20)
#bulb = Press.add_object(2, "Light Bulb")
#state = bulb.add_variable(2, "State of LIght Bulb", False)
#state.set_writable()
print(tempsens)
temper = 20.0
#storing data in sqlite database....
from opcua.server.history_sql import HistorySQLite
#server.iserver.history_manager.set_storage(HistorySQLite("my_datavalue_history5.sql"))

    # starting!


    # enable data change history for this particular node, must be called after start since it uses subscription
#server.historize_node_data_change(Temp, period=None, count=5)
#server.historize_node_data_change(Press, period=None, count=10)
server.start()
try:
        count = 0
        while True:
            sleep(1)
            count += 0.1
            Temp.set_value(math.sin(count))
            Press.set_value(math.cos(count))
            print(math.sin(count))
            print(math.cos(count))

except:
        server.stop()
        print("server offline")
            
"""
try:
        # time.sleep is here just because we want to see events in UaExpert
        import time
        count = 0
        while True:
            time.sleep(5)
            myevgen.event.Message = ua.LocalizedText("MyFirstEvent %d" % count)
            myevgen.event.Severity = count
            myevgen.event.MyNumericProperty = count
            myevgen.event.MyStringProperty = "Property " + str(count)
            myevgen.trigger()
           # mysecondevgen.trigger(message="MySecondEvent %d" % count)
            count += 1

#try:
#        print("Server")
 #       server.start()
	
  #      while True:
		
                #Temperature = 20
                #Pressure =100
                #Temp.set_value(Temperature)
                #Press.set_value(Pressure)               
                #print(Temperature)
                #print(Pressure)
   #             print("GEt Value", Temp.get_value())
                #temp.set_value(temper)
                #print("New temp:", str(temp.get_value()))
                #print("State of Bulb",str(state.get_value()))
    #            sleep(2)
"""


