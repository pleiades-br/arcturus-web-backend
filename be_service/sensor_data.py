import json
import logging

SENSOR_DATA_FILE = "/tmp/safetyrails/sensordata"

def get_sensor_data():
    sensor_data = None
    try:
        with open(SENSOR_DATA_FILE, 'r') as sensor_file:
            sensor_data = json.load(sensor_file)
    except Exception as e:
        logging.error(f'Not possible to get data from file: {SENSOR_DATA_FILE}. Error: {e}')

    if sensor_data is not None:
        sensor_data["status"] = 200
        return sensor_data


    return {'status': 400}
