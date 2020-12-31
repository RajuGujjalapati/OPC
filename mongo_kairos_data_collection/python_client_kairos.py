from opcua import Client
import time
client = Client("opc.tcp://127.0.0.1:5091")
chek = client.connect()


def after_every_minute():
    time.sleep(60)
    print("hoooo")
    client.connect()
    after_conn()

def after_conn():
    print("hey")
    if chek is None:
        # client.connect()
        print("here")
        obj_node = client.get_objects_node()
        print(obj_node)
        se = obj_node.get_children()
        print(se)
        try:
            for i in se[1:]:
                tag_value = i.get_children()
                for tag_data in tag_value:
                    print(tag_data.get_value())
        except Exception as e:
            print("Some Exception", e)
        finally:
            print("po")
            client.close_session()
            # client.close_secure_channel() # getting error if we use this..
            client.disconnect()
            after_every_minute()

after_conn()
