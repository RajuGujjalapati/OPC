import asyncio
import sys
sys.path.insert(0, "..")
import math
import opcua

from asyncua import ua, Server
from asyncua.server.history_sql import HistorySQLite


async def main():

    # setup our server
    server = Server()
    
    # Configure server to use sqlite as history database (default is a simple memory dict)
    server.iserver.history_manager.set_storage(HistorySQLite("my_datavalue_history.sql"))
    
    # initialize server 
    server.init()

    server.set_endpoint("opc.tcp://localhost:5000")

    # setup our own namespace, not really necessary but should as spec
    uri = "http://examples.freeopcua.github.io"
    idx = server.register_namespace(uri)
    print(idx)
    # get Objects node, this is where we should put our custom stuff
    objects = server.nodes.objects
    print(objects)

    # populating our address space
    myobj =  objects.add_object(idx, "MyObject")
    myvar =  myobj.add_variable(idx, "MyVariable", ua.Variant(0, ua.VariantType.Double))
    myfl =  myobj.add_variable(idx, "FLoat", ua.Variant(20.7, ua.VariantType.Float))
    print(myobj)
    print(myvar)
    myvar.set_writable()  # Set MyVariable to be writable by clients
    print(myvar)
    print(myfl)
    custom_etype = server.nodes.base_event_type.add_object_type(2, 'MySecondEvent')
    custom_etype.add_property(2, 'MyIntProperty', ua.Variant(0, ua.VariantType.Int32))
    custom_etype.add_property(2, 'MyBoolProperty', ua.Variant(True, ua.VariantType.Boolean))

    mysecondevgen = server.get_event_generator(custom_etype, myobj)

    # starting!
    server.start()

    # enable data change history for this particular node, must be called after start since it uses subscription
    server.historize_node_data_change(myvar, period=None)
    server.historize_node_data_change(myfl, period=None)
    import random

    try:
        count = 0
        while True:
            asyncio.sleep(1)
            count += 0.1
            mysecondevgen.trigger(message="MySecondEvent %d" % count)
            
            myvar.write_value(math.sin(count))
            myfl.write_value(math.cos(random.randint(1,99)))
            
            count += 1
    finally:
        # close connection, remove subscriptions, etc
            server.stop()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    loop.run_until_complete(main())

