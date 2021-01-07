import json

fields = ['category_1', 'category_2', 'category_3', 'category_4', 'category_5', 'category_6']


def structure_query(raw_dict, dev_ins_id, tag_list):
    gate_way_id, sensor_id = [gate_way_id for i in range(len(tag_list))], [sensor_id for i in range(len(tag_list))]
    site_id, block = [site_id for i in range(len(tag_list))], [block for i in range(len(tag_list))]
    dev_ins_id = [dev_ins_id for i in range(len(tag_list))]
    result = list(zip(site_id, gate_way_id, dev_ins_id, block, tag_list, sensor_id))
    dicts = [dict(zip(fields, d)) for d in result]
    if raw_dict:
        value_list = [{"name": "ilens.live_data.raw", "datapoints": [raw_val], 'tags': cat_dict} for raw_val, cat_dict
                      in zip(raw_dict, dicts)]
        return value_list
    else:
        return None
