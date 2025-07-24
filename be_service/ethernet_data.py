import json
import logging

ETHERNET_CONFIG_FILE = "./tmp/safetyrails/ethernet"


def get_ethernet_config():
    ethernet_config = None
    try:
        with open(ETHERNET_CONFIG_FILE, 'r') as ethernet_file:
            ethernet_config = json.load(ethernet_file)
    except Exception as e:
        logging.error(f'Not possible to get data from file: \
                      {ETHERNET_CONFIG_FILE}. Error: {e}')

    if ethernet_config is not None:
        ethernet_config["status"] = 200
        return ethernet_config

    return {'status': 400}


def post_ethernet_config(ethernet_config):
    try:
        with open(ETHERNET_CONFIG_FILE, 'w') as ethernet_file:
            json.dump(ethernet_config, ethernet_file)
    except Exception as e:
        logging.error(f'Not possible to save data on file: \
                      {ETHERNET_CONFIG_FILE}. Error: {e}')
        return {'status': 400}

    return {'status': 200}
