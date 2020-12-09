import sys
import traceback

sys.path.insert(0, "..")
import logging
import time

try:
    from IPython import embed
except ImportError:
    import code


    def embed():
        vars = globals()
        vars.update(locals())
        shell = code.InteractiveConsole(vars)
        shell.interact()

from opcua import Client
from opcua import ua


class SubHandler(object):
    """
    Subscription Handler. To receive events from server for a subscription
    data_change and event methods are called directly from receiving thread.
    Do not do expensive, slow or network operation there. Create another 
    thread if you need to do such a thing
    """

    def datachange_notification(self, node, val, data):
        print("Python: New data change event", node, val)

    def event_notification(self, event):
        print("Python: New event", event)


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARN)
    # logger = logging.getLogger("KeepAlive")
    # logger.setLevel(logging.DEBUG)

    client = Client("opc.tcp://localhost:5000")

    # client = Client("opc.tcp://OPC@192.168.6.162/Matrikon.OPC.Simulation.1") #connect using a user
    try:
        client.connect()
        client.load_type_definitions()  # load definition of server specific structures/extension objects

        # Client has a few methods to get proxy to UA nodes that should always be in address space such as Root or Objects
        root = client.get_root_node()
        print("Root node is: ", root)
        objects = client.get_objects_node()
        print("Objects node is: ", objects)
        test = root.get_children()
        # Node objects have methods to read and write node attributes as well as browse or populate address space
        print("Children of root are: ", root.get_children())
        print("---------------------------")
        #print(root.get_child("ns=2;i=1"))
        try:
            for i in test:
                get_ = i.get_children()
                print(get_)
                try:
                    for j in get_:
                        get_more_child = j.get_children()
                        print(get_more_child)
                        try:
                            for k in get_more_child:
                                print('*' * 30)
                                res = k.get_children()
                                print([wres.get_browse_name() for wres in res])
                        except:
                            traceback.print_tb()
                except:
                    traceback.print_exception()
        except:
            traceback.print_exc()
            pass
        # get a specific node knowing its node id
        # var = client.get_node(ua.NodeId(1002, 2))
        var = client.get_node("ns=2;i=1")
        # print(var.get_value())
        # var.get_data_value() # get value of node as a DataValue object
        # var.get_value() # get value of node as a python builtin
        # var.set_value(ua.Variant([23], ua.VariantType.Int64)) #set node value using explicit data type
        # var.set_value(3.9) # set node value using implicit data type

        # gettting our namespace idx
        uri = "TEst"
        idx = client.get_namespace_index(uri)
        print(idx)
        # Now getting a variable node using its browse path
        myvar = root.get_children()
        print(myvar)
        obj = root.get_child(["0:Objects", "{}:MyObject".format(idx)])
        print(obj.nodeid)
        print("obj is: ", obj.get_browse_name())
        types = root.get_child(["0:Types", "{}:EventTypes".format(0)])
        print(types.get_children())
        # subscribing to a variable node
        handler = SubHandler()
        # sub = client.create_subscription(1000, handler)
        # print(sub)
        print("_" * 30)
        myevent = root.get_child(["0:Types", "0:EventTypes", "0:BaseEventType", "2:MyFirstEvent"])
        print(myevent)
        obj = root.get_child(["0:Objects", "2:MyObject"])
        sub = client.create_subscription(1000, handler)
        print(ua.ObjectIds.Server)
        handle1 = sub.subscribe_events(obj, myevent)
        # print(handle1)
        # handle = sub.subscribe_data_change(var.get_children()+myevent.get_children())# pass list of nodes for subscription
        # # check = sub.subscribe_events()
        # # print(check)
        # print("Handle", handle)
        time.sleep(0.1)
        # sub.unsubscribe(handle1)
        # client.load_enums()
        # we can also subscribe to events from server
        # sub_evnts = sub.subscribe_events()
        # print(sub_evnts)
        # sub_evnts1 = sub.subscribe_events()
        # print(sub_evnts1)

        # myh = root.get_child(["0:Objects", "2:MyObject"])
        # print(myh)
        # sub.unsubscribe(handle)
        # sub.delete()
        # calling a method on server
        # res = obj.call_method("ns=2;i=2", "True")
        # print("method result is: ", res)
        print("complete")
        embed()
    except Exception as e:
        traceback.print_exc()
        client.disconnect()
