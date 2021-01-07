import json

fields = ['category_1', 'category_2', 'category_3','category_4','category_5', 'category_6']


def structure_query(raw_dict, site_id, gate_way_id, dev_ins_id, block,tag_list, sensor_id):
    gate_way_id, sensor_id = [gate_way_id for i in range(len(tag_list))], [sensor_id for i in range(len(tag_list))]
    site_id, block = [site_id for i in range(len(tag_list))], [block for i in range(len(tag_list))]
    dev_ins_id = [dev_ins_id for i in range(len(tag_list))]
    result = list(zip(site_id, gate_way_id, dev_ins_id, block, tag_list,  sensor_id))
    dicts = [dict(zip(fields, d)) for d in result]
    if raw_dict:
        value_list = [{"name": "ilens.live_data.raw", "datapoints": [raw_val], 'tags': cat_dict} for raw_val, cat_dict in zip(raw_dict,dicts)]
        return value_list
    else :
        return None


def process_raw_data(fuc_name, sensor_dict, mul_list, _date, be=None, signed=None):
    flatten_list = sum(sensor_dict, [])
    values = fuc_name(flatten_list, be) if be in [True, False] else fuc_name(flatten_list, be, signed) if signed in [
        True, False] else fuc_name(flatten_list)
    raw = [value * mul for value, mul in zip(values, list(map(float, mul_list)))]
    raw_data = list(map(lambda x: [_date, x], raw))
    return raw_data


def web_socket_struct(raw_dict, dev_ins_id, tag_list, site_id, gateway_instance, sensor_id, block_id, ws):
    if len(tag_list) == 1:
        return None
    # print('inside websocket')
    dev_ins_id = [dev_ins_id for i in range(len(tag_list))]
    data_list = list(zip(dev_ins_id, tag_list, raw_dict))
    result = {}
    for i in data_list:
        result.setdefault(i[0], {}).update({i[1]: i[2]})
    for dev, val in result.items():
        topic = "ilens/"+site_id+"/"+gateway_instance+"/"+dev+"/"+sensor_id+"/"+"block_"+str(block_id)
        ws.publish(topic, json.dumps(val), retain=True)
        # print("Mqtt Pushed for:", val)


def reg_map(raw, ad_list, tag_list):
    a_list, t_list = ([], [])
    if raw is None:  return a_list, t_list
    for i, tag in zip(ad_list, tag_list):
        if raw[i[0]:i[1]]:
            a_list.append(raw[i[0]:i[1]])
            t_list.append(tag)
    return a_list, t_list
