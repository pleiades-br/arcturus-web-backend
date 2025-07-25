import json
import logging

LTE_CONFIG_FILE = "./tmp/safetyrails/lte"


def get_lte():
    lte_config = None
    try:
        with open(LTE_CONFIG_FILE, 'r') as lte_file:
            lte_config = json.load(lte_file)
    except Exception as e:
        logging.error(f'Not possible to get data from file: \
                      {LTE_CONFIG_FILE}. Error: {e}')

    if lte_config is not None:
        lte_config["status"] = 200
        return lte_config

    return {'status': 400}


def post_lte(lte_config):
    try:
        with open(LTE_CONFIG_FILE, 'w') as lte_file:
            json.dump(lte_config, lte_file)
    except Exception as e:
        logging.error(f'Not possible to save data on file: \
                      {LTE_CONFIG_FILE}. Error: {e}')
        return {'status': 400}

    return {'status': 200}
