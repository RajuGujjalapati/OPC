Python 3.8.3 (tags/v3.8.3:6f8c832, May 13 2020, 22:37:02) [MSC v.1924 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
>>> from opcua import Client
>>> client.connect()
Traceback (most recent call last):
  File "<pyshell#1>", line 1, in <module>
    client.connect()
NameError: name 'client' is not defined
>>> client = Client("opc.tcp://127.0.0.2:12345")
>>> client.connect()
Traceback (most recent call last):
  File "<pyshell#3>", line 1, in <module>
    client.connect()
  File "C:\Users\New\AppData\Local\Programs\Python\Python38\lib\site-packages\opcua\client\client.py", line 272, in connect
    self.connect_socket()
  File "C:\Users\New\AppData\Local\Programs\Python\Python38\lib\site-packages\opcua\client\client.py", line 307, in connect_socket
    self.uaclient.connect_socket(self.server_url.hostname, self.server_url.port)
  File "C:\Users\New\AppData\Local\Programs\Python\Python38\lib\site-packages\opcua\client\ua_client.py", line 266, in connect_socket
    return self._uasocket.connect_socket(host, port)
  File "C:\Users\New\AppData\Local\Programs\Python\Python38\lib\site-packages\opcua\client\ua_client.py", line 155, in connect_socket
    sock = socket.create_connection((host, port), timeout=self.timeout)
  File "C:\Users\New\AppData\Local\Programs\Python\Python38\lib\socket.py", line 808, in create_connection
    raise err
  File "C:\Users\New\AppData\Local\Programs\Python\Python38\lib\socket.py", line 796, in create_connection
    sock.connect(sa)
ConnectionRefusedError: [WinError 10061] No connection could be made because the target machine actively refused it
>>> client = Client("opc.tcp://127.0.0.1:12345")
>>> client.connect()
>>> client.get_namespace_array()
['http://opcfoundation.org/UA/', 'urn:freeopcua:python:server', 'RooM1']
>>> objects = client.get_objects_node()
>>> objects.get_children()
[Node(NumericNodeId(i=2253)), Node(StringNodeId(ns=2;s="TS1")), Node(NumericNodeId(ns=2;i=1))]
>>> bulb = objects.get_children()[2]
>>> tempsens = objects.get_children()[1]
>>> bulb.get_children()
[Node(NumericNodeId(ns=2;i=2))]
>>> state = bulb.get_children()[0]
>>> state.get_value()
False
>>> state.set_value(True)
>>> client.close_session()
>>> 
