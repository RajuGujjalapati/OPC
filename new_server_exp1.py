from opcua import Server

server = Server()
#server.private_key = "See!@#$##**&&^"
import os
print(os.getcwd())
# server.load_private_key(r"C:\Users\New\OneDrive\Desktop\El_Measure\private_key.txt")
# server.disable_clock()
server.set_endpoint("opc.tcp://localhost:5000/freeopcua/server/")
#server.set_endpoint("opc.tcp://0.0.0.0:4840/freeopcua/server/")

server.set_server_name("FreeOpcUa Example Server")

# setup our own namespace
uri = "http://examples.freeopcua.github.io"
idx = server.register_namespace(uri)

# get Objects node, this is where we should put our custom stuff
objects = server.get_objects_node()

# populating our address space
myfolder = objects.add_folder(idx, "myEmptyFolder")
myobj = objects.add_object(idx, "MyObject")
myvar = myobj.add_variable(idx, "MyVariable", 6.7)
myvar.set_writable()  # Set MyVariable to be writable by clients

# starting!
server.start()