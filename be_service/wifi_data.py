import json
import logging

WIFI_CONFIG_FILE = "./tmp/safetyrails/wifi"


def get_wifi():
    wifi_config = None
    logging.info(f"get_ethernet method WIFI data")
    try:
        with open(WIFI_CONFIG_FILE, 'r') as wifi_file:
            wifi_config = json.load(wifi_file)
    except Exception as e:
        logging.error(f'Not possible to get data from file: \
                      {WIFI_CONFIG_FILE}. Error: {e}')

    if wifi_config is not None:
        wifi_config["status"] = 200
        return wifi_config

    return {'status': 400}


def post_wifi(wifi_config):
    try:
        with open(WIFI_CONFIG_FILE, 'w') as wifi_file:
            json.dump(wifi_config, wifi_file)
    except Exception as e:
        logging.error(f'Not possible to save data on file: \
                      {WIFI_CONFIG_FILE}. Error: {e}')
        return {'status': 400}

    return {'status': 200}
