import configparser
import os

CURRENT_CONFIG_PATH_FILE = './tmp/safetyrails/sftrails.conf'
NEW_CONFIG_PATH_FILE = './tmp/safetyrails/sftrails.conf.bkb'
# /etc/sftrails/sftrails.conf


default_config = {
        'MQTT': {
            'host': '',
            'port': 1883,
            'username': '',
            'password': '',
            'topic': 'arc',
            'sleep_timer_s': 60,
        },

        'Sensor Timers': {
            'batt_time': 15,
            'solar_time': 16,
            'barra_in_check_s': 5,
            'ptas_s': 10,
        },

        'Alarm Sensor Thresholds': {
            'barra_v_check_mv': 4000,
            'barra_temperature_c': 60,
            'battery_mv': 10000,
            'solar_pannel': 4500,
            'thres_ptas': 500,
        },

        'Barra wav': {
            'number_files': 0,
            'wav_file1': '',
            'wav_file2': '',
            'wav_file3': '',
            'wav_file4': '',
            'wav_file5': '',
        },

        'PT100 Config': {
            'min_temp': -250,
            'max_temp': 650,
            'rtd_min': 18,
            'rtd_max': 330,
            'rlead_min': 0,
            'rlead_max': 15,
        },
        'Alarm Senson Status': {
            'rail_bar_alarm': False,
            'rail_temp_alarm': False,
            'batt_status': False,
            'solar_status': False,
            'pta1_alarm': False,
            'pta2_alarm': False
            },
    }


def read_config_from_file():
    """
    Read the current configuration from file
    If the file is empty or doesn't exist, returns the default configuration
    """
    curr_file_path = CURRENT_CONFIG_PATH_FILE
    curr_config = configparser.ConfigParser()
    if os.path.exists(curr_file_path) and os.path.getsize(curr_file_path) > 0:
        with open(curr_file_path, 'r') as currConfigFile:
            curr_config.read(currConfigFile)
        print(f"Recoverd current configuration from {curr_file_path} ")
    else:
        print('Current config file not found or is empty. Using default \
              configuration.')
        curr_config.read_dict(default_config)
        with open(curr_file_path, 'w') as config_file:
            curr_config.write(config_file)
    return curr_config


def write_config_to_file(config):
    """
    Write the new configuration to file
    """
    new_file_path = NEW_CONFIG_PATH_FILE
    try:
        with open(new_file_path, 'w') as newConfigFile:
            config.write(newConfigFile)
        print(f"New configuration saved to {new_file_path}")
        return True
    except Exception as error:
        print(f'Not able to create the config file on {new_file_path}\n \
               Error {type(error).__name__} - {error}')
        return False


def mqtt_save_config_file(host,
                          port,
                          username,
                          password,
                          topic,
                          sleep_timer_s):
    """
    Receive the new MQTT config, updates the current config
     and saves to a new file
    """
    curr_config = read_config_from_file()
    if host is not None:
        curr_config['MQTT']['host'] = str(host)
    if port is not None:
        curr_config['MQTT']['port'] = str(port)
    if username is not None:
        curr_config['MQTT']['username'] = str(username)
    if password is not None:
        curr_config['MQTT']['password'] = str(password)
    if topic is not None:
        curr_config['MQTT']['topic'] = str(topic)
    if sleep_timer_s is not None:
        curr_config['MQTT']['sleep_timer_s'] = str(sleep_timer_s)
    return (write_config_to_file(curr_config))


def sensor_save_config_file(batt_time,
                            solar_time,
                            barra_in_check_s,
                            ptas_s,
                            barra_v_check_mv,
                            barra_temperature_c,
                            battery_mv,
                            solar_pannel,
                            thres_ptas,
                            rail_bar_alarm,
                            rail_temp_alarm,
                            batt_alarm,
                            solar_alarm,
                            pta1_alarm,
                            pta2_alarm):
    """
    Receive the new sensors' config, updates the current config
     and saves to a new file
    """
    curr_config = read_config_from_file()
    curr_config['Sensor Timers']['batt_time'] = batt_time
    curr_config['Sensor Timers']['solar_time'] = solar_time
    curr_config['Sensor Timers']['barra_in_check_s'] = barra_in_check_s
    curr_config['Sensor Timers']['ptas_s'] = ptas_s
    curr_config['Alarm Sensor Thresholds']['barra_v_check_mv'] = barra_v_check_mv
    curr_config['Alarm Sensor Thresholds']['barra_temperature_c'] = barra_temperature_c
    curr_config['Alarm Sensor Thresholds']['battery_mv'] = battery_mv
    curr_config['Alarm Sensor Thresholds']['solar_pannel'] = solar_pannel
    curr_config['Alarm Sensor Thresholds']['thres_ptas'] = thres_ptas
    curr_config['Alarm Senson Status']['rail_bar_alarm'] = rail_bar_alarm
    curr_config['Alarm Senson Status']['rail_temp_alarm'] = rail_temp_alarm
    curr_config['Alarm Senson Status']['batt_alarm'] = batt_alarm
    curr_config['Alarm Senson Status']['solar_alarm'] = solar_alarm
    curr_config['Alarm Senson Status']['pta1_alarm'] = pta1_alarm
    curr_config['Alarm Senson Status']['pta2_alarm'] = pta2_alarm
    return (write_config_to_file(curr_config))
