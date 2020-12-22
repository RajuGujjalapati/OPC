data = [445,623
    , 3306
    ,4840
    ,5432
    ,16992
    ,33060
    ,49664
    ,49665
    ,49666
    ,49667,
     49668, 49682,
        1434,
        49674]
import time
from opcua import Client
from opcua.ua.uaerrors import BadCommunicationError
#
# for i in data:
#     try:
client = Client("opc.tpc://localhost:135/Matrikon.OPC.Simulation.1")
print(client.get_endpoints())
    #     print(i)
    #
client.connect()
    #     print(client)
    #     if client == None:
    #         print(i)
    # except Exception as e:
    #     pass
    # except BadCommunicationError or OSError:
    #     print("errr")
    #     pass
    # finally:
    #     try:
    #         client.close_session()
    #         client.close_secure_channel()
    #
    #     except OSError:
    #         client.disconnect()
    #     continue
    # time.sleep(1)
