import sys

sys.path.insert(0, "..")
import logging

try:
    from IPython import embed
except ImportError:
    import code


    def embed():
        vars = globals()
        vars.update(locals())
        shell = code.InteractiveConsole(vars)
        shell.interact()

from opcua import ua, Server

if __name__ == "__main__":
    # logging.basicConfig(level=logging.WARN)
    # logger = logging.getLogger("opcua.server.internal_subscription")
    # logger.setLevel(logging.DEBUG)

    # setup our server
    server = Server()
    server.set_endpoint("opc.tcp://127.0.0.1:5000")

    # setup our own namespace, not really necessary but should as spec
    uri = "TEst"
    idx = server.register_namespace(uri)
    print("idx", idx)
    # get Objects node, this is where we should put our custom stuff
    objects = server.get_objects_node()
    print("objects", objects)
    # populating our address space
    myobj = objects.add_object(idx, "MyObject")
    print("myobj", myobj)
    myvar = myobj.add_variable(idx, "MyVariable", ua.Variant(0.25, ua.VariantType.Double))
    myfl = myobj.add_variable(idx, "FLoat", ua.Variant(20.7, ua.VariantType.Float))
    myfl.set_writable()
    myvar.set_writable()
    # Creating a custom event: Approach 1
    # The custom event object automatically will have members from its parent (BaseEventType)
    etype = server.create_custom_event_type(idx, 'MyFirstEvent', ua.ObjectIds.BaseEventType,
                                            [('MyNumericProperty', ua.VariantType.Float),
                                             ('MyStringProperty', ua.VariantType.Double)])
    print(etype)
    myevgen = server.get_event_generator(etype, myobj)

    # Creating a custom event: Approach 2
    custom_etype = server.nodes.base_event_type.add_object_type(2, 'MySecondEvent')
    custom_etype.add_property(2, 'MyIntProperty', ua.Variant(22, ua.VariantType.Int32))
    custom_etype.add_property(2, 'MyBoolProperty', ua.Variant(True, ua.VariantType.Boolean))
    mysecondevgen = server.get_event_generator(custom_etype, myobj)
    #############Testing
    custom_etype1 = server.nodes.base_event_type.add_object_type(3, 'MySecondEvent3')

    custom_etype1.add_property(2, 'MyIntProperty11', ua.Variant(67, ua.VariantType.Int32))
    custom_etype1.add_property(2, 'MyBoolProperty11', ua.Variant(True, ua.VariantType.Boolean))
    mysecondevgen1 = server.get_event_generator(custom_etype1, myobj)
    # mysecondevgen.trigger("Testing for trigger data")
    # starting!
    server.start()

    try:
        # time.sleep is here just because we want to see events in UaExpert
        import time

        count = 0
        import random

        while True:
            time.sleep(5)
            myvar.set_value(random.randint(1, 900))
            myfl.set_value(random.randrange(1, 800))
            myevgen.event.Message = ua.LocalizedText("MyFirstEvent %d" % count)
            myevgen.event.Severity = count
            myevgen.event.MyNumericProperty = count
            myevgen.event.MyStringProperty = "Property " + str(count)

            mysecondevgen1.event.Message = ua.LocalizedText("Custom Event ra babu %d" % count)
            mysecondevgen1.event.Severity = count
            mysecondevgen1.event.MyNumericProperty = count
            mysecondevgen1.event.MyStringProperty = "Property " + str(count)
            mysecondevgen1.trigger(message="Custom Event message")

            # myevgen.event.Message = ua.LocalizedText("ADSAKJAM AKDNKA KJDASJDAN SKDFJHDKA AKSJHDFNFL")
            # myevgen.trigger()
            myevgen.trigger(message="Raju Check %d" % count)
            # mysecondevgen.trigger(message="MySecondEvent %d" % count)
            # mysecondevgen1.trigger(message="Raju Check %d" % count)
            count += 1

        embed()
    finally:
        # close connection, remove subcsriptions, etc
        server.stop()
