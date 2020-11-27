import sys
import logging
import time
from opcua import Client
from opcua import ua


class SubHandler(object):

    def datachange_notification(self, node, val, data):
        print("Python: New data change event", node, val)

    def event_notification(self, event):
        print("Python: New event", event)


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARN)
    client = Client("opc.tcp://192.168.8.192:48020/", timeout=5)
    client.keepalive = False
    while True:
        try:
            client.connect()
            # client.load_type_definitions()  # load definition of server specific structures/extension objects
            root = client.get_root_node()
            print("Root node is: ", root)
            objects = client.get_objects_node()
            print("Objects node is: ", objects)

            # Node objects have methods to read and write node attributes as well as browse or populate address space
            print("Children of root are: ", root.get_children())

            myvar = client.get_node("ns=2;i=13")
            print(myvar.get_value())
            handler = SubHandler()
            sub = client.create_subscription(500, handler)
            handle = sub.subscribe_data_change(myvar)
            is_connected = True
            while True:
                if not client.uaclient._uasocket._thread.isAlive():
                    raise Exception
        except:
            print("Disconnected")
            try:
                client.disconnect()
            except:
                pass
        time.sleep(1)
