import uuid
from threading import Thread
import copy
import logging
from datetime import datetime
import time
from math import sin
import sys
from opcua.ua import NodeId, NodeIdType
from opcua import ua, uamethod, Server

if __name__ == "__main__":
    # optional: setup logging
    logging.basicConfig(level=logging.WARN)
    # logger = logging.getLogger("opcua.address_space")
    # logger.setLevel(logging.DEBUG)
    # logger = logging.getLogger("opcua.internal_server")
    # logger.setLevel(logging.DEBUG)
    # logger = logging.getLogger("opcua.binary_server_asyncio")
    # logger.setLevel(logging.DEBUG)
    # logger = logging.getLogger("opcua.uaprocessor")
    # logger.setLevel(logging.DEBUG)

    # now setup our server
    # server = Server()
    # #server.disable_clock()
    # #server.set_endpoint("opc.tcp://localhost:4840/freeopcua/server/")
    # server.set_endpoint("opc.tcp://0.0.0.0:4840/freeopcua/server/")
    #
    # server.load_certificate("certificate.pem")
    # server.load_private_key("key.pem")
    # server.set_security_policy([
    #     # ua.SecurityPolicyType.NoSecurity,
    #     # ua.SecurityPolicyType.Basic128Rsa15_Sign,
    #     # ua.SecurityPolicyType.Basic128Rsa15_SignAndEncrypt,
    #     # ua.SecurityPolicyType.Basic256Sha256_Sign,
    #     ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt
    # ])
    # server.set_endpoint("opc.tcp://localhost:5000")
    # server.set_server_name("FreeOpcUa Example Server")
    # # set all possible endpoint policies for clients to connect through
    #
    # # setup our own namespace
    # uri = "http://examples.freeopcua.github.io"
    # idx = server.register_namespace(uri)
    server = Server()

    endpoint = "opc.tcp://127.0.0.1:5600"
    server.set_endpoint(endpoint)

    servername = "Python-OPC-UA"
    server.set_server_name(servername)
    address_space = server.register_namespace("http://andreas-heine.net/UA")

    uri = "URI:urn:opcua:python:server"
    server.set_application_uri(uri)

    server.load_certificate("certificate.pem")
    server.load_private_key("key.pem")
    server.set_security_policy([
        # ua.SecurityPolicyType.NoSecurity,
        # ua.SecurityPolicyType.Basic128Rsa15_Sign,
        # ua.SecurityPolicyType.Basic128Rsa15_SignAndEncrypt,
        # ua.SecurityPolicyType.Basic256Sha256_Sign,
        ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt
    ])
    idx = server.register_namespace(uri)

    # create a new node type we can instantiate in our address space
    dev = server.nodes.base_object_type.add_object_type(idx, "MyDevice")  ############## learn test_modelling_rule
    dev.add_variable(idx, "sensor1", 1.0).set_modelling_rule(True)  #############
    dev.add_property(idx, "device_id", "0340").set_modelling_rule(True)  ###############
    ctrl = dev.add_object(idx, "controller")  #######################
    ctrl.set_modelling_rule(True)  ######################
    ctrl.add_property(idx, "state", "Idle").set_modelling_rule(True)  #############

    # populating our address space

    # First a folder to organise our nodes
    myfolder = server.nodes.objects.add_folder(idx, "myEmptyFolder")
    # instanciate one instance of our device
    mydevice = server.nodes.objects.add_object(idx, "Device0001", dev)
    mydevice_var = mydevice.get_child(
        ["{}:controller".format(idx), "{}:state".format(idx)])  # get proxy to our device state variable
    print(mydevice_var)
    # create directly some objects and variables
    myobj = server.nodes.objects.add_object(idx, "MyObject")  ########################MAIN OBJECT
    myvar = myobj.add_variable(idx, "MyVariable", 6.7)  ######################
    print(myvar)
    mysin = myobj.add_variable(idx, "MySin", 0, ua.VariantType.Float)  ###########################
    myvar.set_writable()  # Set MyVariable to be writable by clients
    mystringvar = myobj.add_variable(idx, "MyStringVariable", "Really nice string")  ###########################
    mystringvar.set_writable()  # Set MyVariable to be writable by clients
    myguidvar = myobj.add_variable(NodeId(uuid.UUID('1be5ba38-d004-46bd-aa3a-b5b87940c698'), idx, NodeIdType.Guid),
                                   'MyStringVariableWithGUID', 'NodeId type is guid')  #########################
    mydtvar = myobj.add_variable(idx, "MyDateTimeVar", datetime.utcnow())  #######################
    mydtvar.set_writable()  # Set MyVariable to be writable by clients
    myarrayvar = myobj.add_variable(idx, "myarrayvar", [6.7, 7.9])  ##########################
    myarrayvar = myobj.add_variable(idx, "myStronglytTypedVariable",
                                    ua.Variant([], ua.VariantType.UInt32))  #########################
    print(myarrayvar)
    myprop = myobj.add_property(idx, "myproperty", "I am a property")
    mymethod = myobj.add_method(idx, "mymethod", 200, [ua.VariantType.Int64], [ua.VariantType.Boolean])
    multiply_node = myobj.add_method(idx, "multiply", 600, [ua.VariantType.Int64, ua.VariantType.Int64],
                                     [ua.VariantType.Int64])

    # import some nodes from xml
    # server.import_xml("custom_nodes.xml")

    # creating a default event object
    # The event object automatically will have members for all events properties
    # you probably want to create a custom event type, see other examples
    myevgen = server.get_event_generator()
    # custom_etype = server.nodes.base_event_type.add_object_type(2, 'MySecondEvent')
    # custom_etype.add_property(2, 'MyIntProperty', ua.Variant(0, ua.VariantType.Int32))
    # custom_etype.add_property(2, 'MyBoolProperty', ua.Variant(True, ua.VariantType.Boolean))

    # mysecondevgen = server.get_event_generator(custom_etype, myobj)

    # starting!
    server.start()
    try:
        # time.sleep is here just because we want to see events in UaExpert
        import time

        count = 0
        while True:
            time.sleep(5)
            myevgen.event.Message = ua.LocalizedText("MyFirstEvent %d" % count)
            myevgen.event.Severity = count
            myevgen.event.MyNumericProperty = count
            print(myevgen)
            myevgen.event.MyStringProperty = "Property " + str(count)
            myevgen.trigger()
            # mysecondevgen.trigger(message="MySecondEvent %d" % count)
            # print(mysecondevgen)
            # mysecondevgen.trigger(message="MySecondEvent %d" % count)
            count += 1
    except Exception as e:
        print(e)
    finally:
        # vup.stop()
        server.stop()
