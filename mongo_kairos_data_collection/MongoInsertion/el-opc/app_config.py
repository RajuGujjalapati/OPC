import yaml
import logging
import sys


class AppConfig:
    def __init__(self):
        config_path = r"C:\Users\New\Downloads\opc-test (1)\config.yml"
        with open(config_path, 'r') as ymlFile:
            self.cfg = yaml.load(ymlFile, Loader=yaml.FullLoader)

    def get_mongo_host(self):
        return self.cfg['mongo_db']['mongo_connection']

    def get_mongo_uri(self, db_name):
        return self.cfg['mongo_db']['mongo_connection'] + '/' + db_name

    def get_kairos_host(self):
        return self.cfg['kairos_db']['url']

    def get_mqtt_host(self):
        return self.cfg['mqtt']['host'], int(self.cfg['mqtt']['port'])

    def get_web_socket_host(self):
        return self.cfg['mqtt_web_socket']['host'], int(self.cfg['mqtt_web_socket']['port'])


def configure_logging():
    # create logger
    logger = logging.getLogger()
    logger.setLevel((6 - int(6)) * 10)

    # remove default logger
    while logger.handlers:
        logger.handlers.pop()

    # create file handler which logs even debug messages
    fh = logging.FileHandler('debug_logs')
    fh.setLevel(logging.DEBUG)

    # create console handler with different format
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)

    # create formatters and add it to the handlers
    f1 = logging.Formatter('[%(levelname)s’]\t - %(asctime)s - %(name)s - %(message)s')
    f2 = logging.Formatter('[%(levelname)s]\t %(message)s  - %(filename)s: %(funcName)s(): %(lineno)d:\t ')
    f2_simple = logging.Formatter('[%(levelname)s]\t [%(threadName)s]\t %(message)s')
    fh.setFormatter(f2_simple)
    ch.setFormatter(f2_simple)

    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)
