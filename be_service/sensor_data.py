import os
import json
import logging

SENSOR_DATA_FILE = "/tmp/safetyrails/sensordata"

def get_sensor_data():
    sensor_data = None
    try:
        with os.open(SENSOR_DATA_FILE, 'r') as sensor_file:
            sensor_data = json.load(sensor_file)
    except Exception as e:
        logging.error(f'Not possible to get data from file: {SENSOR_DATA_FILE}. Error: {e}')

    if sensor_data is not None:
        return {
           "rail": {
                "bar_alarm": sensor_data["external_alarms"]["bar_in"],
                "bar_vcc": sensor_data["vcc_bar_sensor"]["vcc_bar"],
                "temp": sensor_data["temp_bar_sensor"]["temperature_bar_ch1"],
            },

            "power": {
                "batt": sensor_data["power_supply"]["battery"],
                "solar": sensor_data["power_supply"]["solar_cel"],
            },

            "hw": {
                "temp": sensor_data["temp_hw"],
                "humi": sensor_data["humi_hw"],
                "j3_alarm": sensor_data["external_alarms"]["pta1"],
                "j4_alarm": sensor_data["external_alarms"]["pta2"]
            }
        }

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
                "j3_alarm": "error",
                "j4_alarm": "error"
            }
    }
