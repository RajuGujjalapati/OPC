import json

from utils.parse_mqtt import *
from opcua import Client
import paho.mqtt.client as mqtt
import time
from app_config import AppConfig
import threading
import socket
import queue


class Device:
    def __init__(self, url):
        self.dev = Client(url)
        self.dev.connect()
        # self.dev = Client("opc.tcp://com_sam:Elmeasure@192.168.5.254:4840/test")

    """~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ READ METHODS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""

    def test(self):
        obj = self.dev.get_objects_node().get_children()  # [1:]
        obj = [i.get_children() for i in obj]
        # print([s.getName for s in obj[0]])
        for _ in obj:
            total_data = []
            all_tags = []
            for i in _:

                try:
                    s = i.get_value()
                    name = i.get_browse_name()
                    total_data.append(s)
                    all_tags.append(str(name).split(':')[1][:-1])
                    # print(s, str(name).split(':')[1][:-1])

                except Exception:
                    traceback.print_exc()
                    pass

        return total_data, all_tags

    def read_raw_values(self, node_id=None):
        try:
            # node = self.dev.get_node(node_id)
            # # node = self.dev.get_node("ns=1;i=4")
            # data = node.get_children()
            # tes = [_.get_children() for _ in data][0]
            # values = self.dev.get_node(str(tes)).get_value()
            obj = self.dev.get_objects_node().get_children()  # [1:]
            obj = [i.get_children() for i in obj][0]
            # for _ in obj:
            see = self.dev.get_values(obj)
            print(see)
            # for i in _:
            #     try:
            #         values= i.get_value()
            # return values
        except Exception:
            traceback.print_exc()


device = Device("opc.tcp://127.0.0.1:5091")
# raw_int = device.test()


class MqttClient:

    def __init__(self, host, port):
        # def __init__(self, host, port, enable_ssl, ssl_location,):

        self.client = mqtt.Client()
        self.queue = queue.Queue()

        # self.client.username_pw_set(service_id, password)
        # if enable_ssl:
        #     self.client.tls_set(ssl_location, tls_version=ssl.PROTOCOL_TLSv1)
        self.client.connect(host, int(port), 60)

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.subTopics = set()

        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        threading.current_thread().setName("MqttClient")
        if rc == 0:
            print("Connected to broker")
            global Connected  # Use global variable
            Connected = True  # Signal connection
        else:
            print("Connection failed")

    def on_message(self, client, userdata, msg):
        # logging.debug("Got mesage from topic: " + str(msg.topic))
        # print(msg)
        self.queue.put(msg.payload.decode())

    def get_queue(self):
        return self.queue

    def publish(self, topic, payload):
        # logging.info('MqttClient: publishing message ' + topic + ':' + payload)
        # self.client.publish(msg["topic"], msg["message"], retain = True)
        self.client.publish(topic, payload, retain=True)

    def stop(self):
        self.client.loop_stop()

    def subscribe(self, topic):
        self.subTopics.add(topic)
        self.client.subscribe(topic)


app_config = AppConfig()
broker_address, _port = app_config.get_mqtt_host()

# start mqtt client
mqtt_client = MqttClient(host=broker_address, port=_port)
status_topic = 'ilens/live/data/'

mqtt_client.subscribe(status_topic)
config = Config()
config.mongo_query()
gate_ways = config.gateway_dict
device_config = config.sensor_collection


# for gate_way in gate_ways:
def publish_data(gate_way):
    print("hiiiiiiiiiii", gate_way)
    # device = Device("opc.tcp://com_sam:Elmeasure@192.168.5.254:4840/test")
    # gate_way = gate_ways.get( 'gateway_instance_10003')
    x = gate_way.get('instance_id')
    var_devices = device_config.get(x)
    for com_id, asset_conf in var_devices.items():
        for block, asset in asset_conf.items():
            start = asset.get('start')
            end = asset.get('end')
            block = block
            site_id = asset.get('site_id')
            sensor_id = asset.get('sensor_id')
            try:
                raw_int,tag_list = device.test() #our method to get data
                print("+"*100)
                print(raw_int, tag_list)
            except Exception:
                traceback.print_exc()
                print('retrying')
                raw_int,tag_list = device.test()
            # tag_list = None
            cure_time = get_millisecond_from_date_time(datetime.now().replace(microsecond=00))
            # cure_time = get_millisecond_from_date_time(datetime.now().replace(second=00, microsecond=00))
            tag_10 = 1 if raw_int else 0
            data = {"values": raw_int, "tag_list" : tag_list,"timestamp": cure_time, 'block': block, 'com_id': com_id,
                    "industry_id": site_id, "gateway_id": x, "sensor_id": sensor_id, "data_logging_frequency": 60,
                    "tag_100081": tag_10}
            print('hoppp',data)
            mqtt_client.publish(status_topic, json.dumps(data))


class ServiceExit(Exception):
    pass


def service_shutdown(signum, frame):
    print('Caught signal %d' % signum)
    raise ServiceExit


# # Define stop action
# def signal_handler():
#     # logging.info('Received kill signal ..Stopping service daemon')
#     global running
#     running = False
#     if "mqtt_client" in globals():
#         mqtt_client.stop()60


running = True


def repeat_():
    while running:
        threads = []
        s = 0
        for i, dev in enumerate(gate_ways):
            if dev.get('instance_id') == 'gateway_instance_10003':

                i = s
                s = s+1
                print("Starting process for portion %s" % (dev))
                threads.append(threading.Thread(target=publish_data, args=[dev, ]))
                threads[i].setDaemon(True)
                threads[i].start()
        time.sleep(60)


if __name__ == '__main__':

    def d_thread(payload):
        toi = threading.Thread(target=process_pay, args=[payload])
        toi.daemon = True
        toi.start()


    try:
        # for thread
        t = threading.Thread(target=repeat_)
        t.start()

        while running:
            try:
                msg = mqtt_client.get_queue().get(timeout=.01)
                d_thread(msg)

            except queue.Empty:
                continue
            except:
                traceback.print_exc()
    except KeyboardInterrupt:
        running = False

        exit()
    #
