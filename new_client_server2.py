from opcua import Client
client  = Client("opc.tcp://localhost:5001/freeopcua/server/")
client.connect()
import traceback
obj  = client.get_objects_node()
#print(obj)
var = obj.get_children()# Main Nodes
print(var)
for v in var:
    print(v.get_browse_name())
    all_child =  v.get_children()
    print(all_child)
    for i in all_child:
        try:            
            com_tom = client.get_node(i).get_value()
            if com_tom != None:
                print(com_tom)
        except:
            """Initially We are getting the values of all nodes if there is any exception we are handling using pass
            The Exception occusrs if there is no value for node (or) if it is a system node (or) the node itself has many children's """
            #pass
            try:
                """As of now there is no use with this(finding the sub children within children
                Instead of this try to get the all node ns and i number and the total i's
                and parse data(if data is only req...
                else go for every main node and get data from that..."""
                for j in all_child:
                    set_up_new = j.get_children()
                    child_child = [client.get_node(str(i)).get_value() for se in set_up_new]
                    for data in child_child:
                        if data==True:

                            print(data)
                        else:
                            pass
            except:
            # #traceback.print_exc()
                pass

print("Over")
print(client.get_node("ns=2;i=11").get_value())
print(client.get_node("ns=2;i=12").get_browse_name())
    # total_child = v.get_children()
    # if len(total_child)>1:
    #     further_child = [_.get_children() for _ in total_child]
        #print(further_child)
        #print(20*'*')


# NO USE
# for i in further_child:
#     res = [client.get_node(str(ui)) for ui in i]
#     print([re.get_value() for re in res])
#print(client.get_node("ns=2;i=11").get_value())
#print(client.get_node("ns=2;i=21").get_browse_name())
