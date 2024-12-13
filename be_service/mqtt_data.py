import json
import logging

MQTT_DATA_FILE = "/tmp/safetyrails/mqtt"

def get_mqtt_data():
    mqtt_data = None
    try:
        with open(MQTT_DATA_FILE, 'r') as mqtt_file:
            mqtt_data = json.load(mqtt_file)
    except Exception as e:
        logging.error(f'Not possible to get data from file: {SENSOR_DATA_FILE}. Error: {e}')

    if mqtt_data is not None:
        mqtt_data["status"] = 200
        return mqtt_data


    return {'status': 400}
