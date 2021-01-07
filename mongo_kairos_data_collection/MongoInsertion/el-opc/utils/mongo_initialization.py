from app_config import AppConfig
from collections import defaultdict
from pymongo import MongoClient, DESCENDING
from tzlocal import get_localzone
"Check the mongo uri (host and port) then connect with yr db and collection with necessary docs."
app_conf = AppConfig()

mongo = MongoClient(app_conf.get_mongo_host())
my_db = mongo['ilens_metadata']

def data_type_struct(s, sensor_dict, tags_data):
    if 'tag_list' not in sensor_dict.keys():
        sensor_dict['tag_list'] = []
    if 'mul_list' not in sensor_dict.keys():
        sensor_dict['mul_list'] = []
    if 'add_list' not in sensor_dict.keys():
        sensor_dict['add_list'] = []
    if 'reg_Address' not in sensor_dict.keys():
        sensor_dict['reg_Address'] = []
    sensor_dict['add_list'].append(s)
    sensor_dict['tag_list'].append(tags_data['tag_id'])
    sensor_dict['reg_Address'].append(tags_data['reg_Address'])
    sensor_dict['mul_list'].append(tags_data['mFactorValue'])


class Config:
    def __init__(self):
        self.gateway_dict = []
        self.instance_id_list = []
        self.sensor_collection = {}
        self.time_zone = None

    def mongo_query(self):
        for time_zone in my_db.industry.find({"isdeleted": {"$in": [False, "false"]}},{"site_info.timezone": 1, "_id": 0}, sort=[('_id', DESCENDING)]):
            self.time_zone = time_zone.get('site_info').get('timezone') if time_zone else str(get_localzone())
        count = 0
        for gateway in my_db.gateway_instance.find({"isdeleted": {"$in": [False, "false"]}, "isdisabled": {"$in": [False, "false"]},"type": "gateway_type_2"}):
            gt_dict = {'name': gateway.get('gatewayname'), 'host': gateway.get('host'), 'port': gateway.get('port'),
                       'time_out': gateway.get('timeout'), 'instance_id': gateway.get('gateway_instance_id')}
            self.gateway_dict.append(gt_dict)
            self.instance_id_list.append(gateway.get('gateway_instance_id'))
            count = count + 1

        sensor_dict = defaultdict(dict)
        for _id in self.instance_id_list:
            sensor_dict[_id] = {}
            # change sensor(collection name) to our coll
            for data in my_db.sensor.find({"general_info.gateway_instance_id": _id}):
                if not data: break
                site_id = data.get('site_id')
                sensor_id = data.get('device_instance_id')
                if data.get('general_info').get('isdeleted') in ["false", False] and data.get('general_info').get(
                             'isdisabled') in ["false", False]:

                    for inside_data in data.get('deviceConfig'):
                        start = int(inside_data['startAddress'])
                        end = int(inside_data['noOfRegister'])
                        virtual_list = []
                        u_id = int(data.get('general_info').get('device_com_id'))
                        block = inside_data.get('blockNumber')
                        if u_id not in sensor_dict[_id].keys():
                            sensor_dict[_id][u_id] = {}
                        if block not in sensor_dict[_id][u_id].keys():
                            sensor_dict[_id][u_id][block] = {}
                            sensor_dict[_id][u_id][block]['start'] = start
                            sensor_dict[_id][u_id][block]['end'] = end
                            sensor_dict[_id][u_id][block]['block'] = block
                            sensor_dict[_id][u_id][block]['com_id'] = u_id
                            sensor_dict[_id][u_id][block]['site_id'] = site_id
                            sensor_dict[_id][u_id][block]['sensor_id'] = sensor_id

                        if inside_data.get('modBusFc') == 'ir':
                            temp = defaultdict(dict)
                            for tags_data in inside_data.get('tagsData'):
                                if tags_data['device_instance_id'] not in temp.keys():
                                    temp[tags_data['device_instance_id']] = {}
                                if tags_data.get('data_Type') == 'float':
                                    if 'float_' not in temp[tags_data['device_instance_id']].keys():
                                        temp[tags_data['device_instance_id']]['float_'] = {}
                                    s = [(int(tags_data['reg_Address']) - start), (int(tags_data['reg_Address']) - start) + 2]
                                    data_type_struct(s, temp[tags_data['device_instance_id']]['float_'], tags_data)

                                elif tags_data.get('data_Type') == 'swapped-float':
                                    if 'swapped-float' not in temp[tags_data['device_instance_id']].keys():
                                        temp[tags_data['device_instance_id']]['swapped-float'] = {}
                                    s = [(int(tags_data['reg_Address']) - start),(int(tags_data['reg_Address']) - start) + 2]
                                    data_type_struct(s, temp[tags_data['device_instance_id']]['swapped-float'], tags_data)

                                elif tags_data.get('data_Type') == 'integer':
                                    if 'integer' not in temp[tags_data['device_instance_id']].keys():
                                        temp[tags_data['device_instance_id']]['integer'] = {}
                                    s = [(int(tags_data['reg_Address']) - start),(int(tags_data['reg_Address']) - start) + 1]
                                    data_type_struct(s, temp[tags_data['device_instance_id']]['integer'], tags_data)

                                elif tags_data.get('data_Type') == 'long-int':
                                    if 'long-int' not in temp[tags_data['device_instance_id']].keys():
                                        temp[tags_data['device_instance_id']]['long-int'] = {}
                                    s = [(int(tags_data['reg_Address']) - start),(int(tags_data['reg_Address']) - start) + 2]
                                    data_type_struct(s, temp[tags_data['device_instance_id']]['long-int'], tags_data)

                                elif tags_data.get('data_Type') == 'unsigned-integer':
                                    if 'unsigned-integer' not in temp[tags_data['device_instance_id']].keys():
                                        temp[tags_data['device_instance_id']]['unsigned-integer'] = {}
                                    s = [(int(tags_data['reg_Address']) - start),(int(tags_data['reg_Address']) - start) + 1]
                                    data_type_struct(s, temp[tags_data['device_instance_id']]['unsigned-integer'], tags_data)

                                elif tags_data.get('data_Type') == 'swapped-long-int':
                                    if 'swapped-long-int' not in temp[tags_data['device_instance_id']].keys():
                                        temp[tags_data['device_instance_id']]['swapped-long-int'] = {}
                                    s = [(int(tags_data['reg_Address']) - start), (int(tags_data['reg_Address']) - start) + 2]
                                    data_type_struct(s, temp[tags_data['device_instance_id']]['swapped-long-int'], tags_data)

                                elif tags_data.get('data_Type') == 'double':
                                    if 'double' not in temp[tags_data['device_instance_id']].keys():
                                        temp[tags_data['device_instance_id']]['doublet'] = {}
                                    s = [(int(tags_data['reg_Address']) - start),(int(tags_data['reg_Address']) - start) + 4]
                                    data_type_struct(s, temp[tags_data['device_instance_id']]['double'], tags_data)

                                elif tags_data.get('data_Type') == 'swapped-double':
                                    if 'swapped-double' not in temp[tags_data['device_instance_id']].keys():
                                        temp[tags_data['device_instance_id']]['doublet'] = {}
                                    s = [(int(tags_data['reg_Address']) - start),(int(tags_data['reg_Address']) - start) + 4]
                                    data_type_struct(s, temp[tags_data['device_instance_id']]['swapped-double'], tags_data)
                            sensor_dict[_id][u_id][block]['dev_list'] = temp
        self.sensor_collection = sensor_dict
        print(sensor_id)


