from opcua import Server

server = Server()
server.set_endpoint("opc.tcp://http://192.168.5.254/192.168.5.254:beck_gw_opc_ua:4840")
print("success")
print(server.get_application_uri())