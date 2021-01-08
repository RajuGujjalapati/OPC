# from kairos import Kairos
#
# db_conn = Kairos()
# print(db_conn.get_kairos_data())
# db_conn.set_metrics_tags = 21312
# db_conn.update_kairos_data()
# print(db_conn.query["metrics"][0]["tags"])
# print(db_conn.response)
# import asyncio, time
#
#
# async def main():
#     print("started async")
#     strt = time.time()
#     task1 = asyncio.create_task(loop_fun1())
#     task2 = asyncio.create_task(loop_fun())
#     # await loop_fun()
#     # await task1
#     # await task2
#     # end1 = time.time()
#     # print(end1 - strt)
#     await loop_fun()
#     await loop_fun1()
#
#
#     end2 = time.time()
#
#     print(end2 - strt)
#     print("completed")
#
#
# async def loop_fun():
#     for i in range(1000000000):
#         if i == 997999999:
#             print(i)
#
#
# async def loop_fun1():
#     for i in range(1000000000):
#         if i == 997999999:
#             print(i)
#
#
# asyncio.run(main())

from opcua import Client, ua

# url = "opc.tcp://127.0.0.1:5600"  # opc.tcp://192.168.4.181:4840
url = "opc.tcp://com.tom:Elmeasure@192.168.4.181:4840/test"
client = Client(url)

client.application_uri = "urn:com-tom:OpcUaServer"
# client.set_user("com.tom")
# client.set_password("Elmeasure")
client.set_security_string(r"Basic256Sha256,SignAndEncrypt,"
                           r"C:\Users\New\OneDrive\Desktop\El_Measure\test_sessionOpenssl\clean\comtom\cert.der,"
                           r"C:\Users\New\OneDrive\Desktop\El_Measure\test_sessionOpenssl\clean\comtom\key.pem")
 # not necessary

client.connect()
print(f"Connected to: {client.get_endpoints()}")

obj = client.get_objects_node()
print(obj.get_children())

# servicelevel_node = client.get_node("ns=0;i=2267")
#
# servicelevel_node_value = servicelevel_node.get_value()
# print(servicelevel_node_value)
#
# client.disconnect()