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
        logging.debug(sensor_data)
        logging.debug(type(sensor_data))
        return sensor_data


    return {
           "rail": {
                "bar_alarm": "error",
                "bar_vcc": "error",
                "temp": "error",
            },

            "power": {
                "batt": "error",
                "solar": "error",
            },

            "hw": {
                "temp": "error",
                "humi": "error",
                "j3_vcc": "error",
                "j4_vcc": "error",
                "pta1_alarm": "error",
                "pta2_alarm": "error"
            }
    }
