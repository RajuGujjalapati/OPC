import yaml


class AppConfig:
    def __init__(self):
        config_path = "config.yml" #/home/elmpc/PycharmProjects/elnet-7.0-py-services/config.yml
        with open(config_path, 'r') as ymlFile:
            self.cfg = yaml.load(ymlFile, Loader=yaml.FullLoader)

    def get_mongo_host(self):
        return self.cfg['mongo_db']['mongo_connection']

    def get_mongo_uri(self, db_name):
        return self.cfg['mongo_db']['mongo_connection'] + '/' + db_name

    def get_kairos_host(self):
        return self.cfg['kairos_db']['url']

    def get_report_file_path(self):
        return self.cfg['service']['mnt_path']

    def get_kl_url(self):
        return self.cfg['service']['kl_url']

    def get_service(self):
        return self.cfg['service']

    def get_schedule(self):
        return self.cfg['scheduler']

    def get_mqtt_host(self):
        return self.cfg['mqtt']['host'], int(self.cfg['mqtt']['port'])

    def get_logs_path(self, path=None, level=None, ):
        if path:
            return self.cfg['log']['path']
        elif level:
            return self.cfg['log']['level']

    def get_meta_service_port(self):
        return self.cfg['service']['port']

    def get_environment(self):
        return self.cfg['environment']['mode']

    def get_token_expiry(self):
        return self.cfg["tokens_expiry"]

    def get_license_path(self):
        return self.cfg["service"]["license_path"]

    def get_sag_swell_tag(self):
        return self.cfg["sag_swell_interruption"]

    def get_plant_incomer_and_distribution_device_group(self):
        return self.cfg['plant_wise_energy_report']

    def get_plant_tags(self):
        return self.cfg['plant_wise_energy_report']['tags']

    def plant_report_mail_list(self):
        return  self.cfg['plant_wise_energy_report']['mail_list']

    def eb_incomer_and_dg_run_hour_tag(self):
        return  [self.cfg['plant_wise_energy_report']['eb_incomer']['tag_id'],self.cfg['plant_wise_energy_report']['dg_run_hours']['tag_id']]

    def get_eb_incomer_device_group_list(self):
        return self.cfg['plant_wise_energy_report']['eb_incomer']['device_group_id_list']

    def get_dg_run_hour_device(self):
        return self.cfg['plant_wise_energy_report']['dg_run_hours']['id']

    def get_plant_report_shift_timing(self):
        return self.cfg['plant_wise_energy_report']['shift_timings']

    def get_timezone(self):
        return self.cfg['timezone']['time_zone']

    # def image_view(self):
    #     return self.cfg['image_view']['image_path']
    #
    # def table_row(self):
    #     return self.cfg["table_row_count"]["count"]
    #
    # def get_hpcl_daily_report_tags(self):
    #     return self.cfg['hpcl_daily_report']['tags']
    #
    # def get_hpcl_daily_report_consumption_device_groups(self):
    #     return self.cfg['hpcl_daily_report']['power_consumption']
    #
    # def get_hpcl_daily_report_breakeup_device_group(self):
    #     return self.cfg['hpcl_daily_report']['power_consumption_breakup']
    #
    # def get_hpcl_daily_report_chiller_runhour_device(self):
    #     return self.cfg['hpcl_daily_report']['chiller_run_hour']
    #
    # def get_hpcl_daily_report_dg_runhour_device(self):
    #     return self.cfg['hpcl_daily_report']['equipment_details']
    #
    # def get_hpcl_specific_fuel_consumption_tags(self):
    #     return self.cfg['specific_fuel_consumption']['tags']
    #
    # def get_hpcl_specific_fuel_consumption_devices(self):
    #     return self.cfg['specific_fuel_consumption']['device_groups']
    #
    # def get_hpcl_daily_report_manual_entry_data(self):
    #     return self.cfg['hpcl_daily_report']['manual_entry_data']
    #
    # def get_hpcl_site_id(self):
    #     return self.cfg['hpcl_daily_report']['site_id']
    #
    # def get_hpcl_specific_fuel_report_manual_entry_id(self):
    #     return self.cfg['specific_fuel_consumption']['manual_entry_id']
    #
    # def get_hpcl_mail_list(self):
    #     return self.cfg['hpcl_daily_report']['mail_list']
    # def get_specific_fuel_report_mail_list(self):
    #     return self.cfg['specific_fuel_consumption']['mail_list']
    #
    # def get_hpcl_report_tempate(self):
    #     return self.cfg['hpcl_daily_report']['template_path']