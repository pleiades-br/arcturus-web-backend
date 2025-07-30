import json
import logging

MQTT_DATA_FILE = "./tmp/safetyrails/mqtt"


def get_mqtt_data():
    mqtt_data = None
    logging.info(f"get_mqtt_data method MQTT data")
    try:
        with open(MQTT_DATA_FILE, 'r') as mqtt_file:
            mqtt_data = json.load(mqtt_file)
    except Exception as e:
        logging.error(f'Not possible to get data from file: \
                      {MQTT_DATA_FILE}. Error: {e}')

    if mqtt_data is not None:
        mqtt_data["status"] = 200
        return mqtt_data

    return {'status': 400}


def post_mqtt(mqtt_data):

    logging.info(f"Received POST body: {mqtt_data}")
    try:
        with open(MQTT_DATA_FILE, 'w') as mqtt_file:
            json.dump(mqtt_data, mqtt_file)
    except Exception as e:
        logging.error(f'Not possible to save data on file: \
                      {MQTT_DATA_FILE}. Error: {e}')
        return {'status': 400}

    return {'status': 200}
