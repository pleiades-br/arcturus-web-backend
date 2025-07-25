from http.server import HTTPServer, BaseHTTPRequestHandler
import network_ifaces as netif
import sensor_data
import ethernet_data
import wifi_data
import lte_data
import mqtt_data
import json
import logging


class Path():
    SENSORS_DATA = "/api/sensors_data"
    CONFIG_ETH = "/api/ethernet"
    CONFIG_WIFI = "/api/wifi"
    CONFIG_LTE = "/api/lte"
    CONFIG_MQTT = "/api/mqtt"
    CONFIG_SENSORS = "/api/sensors_config"


class Response():
    DEFAULT_RESPONSE = {"status": False, "message": "No path found"}


class Server(HTTPServer):
    def __init__(self, server_address, request_handler, paths, response) -> None:
        super().__init__(server_address, request_handler)
        self.path = paths
        self.response = response


class RequestHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server_class) -> None:
        self.server_class = server_class
        super().__init__(request, client_address, server_class)

    def _set_headers(self):
        # Set CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')  # Allow all origins
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def do_GET(self):
        if self.path == self.server_class.path.SENSORS_DATA:
            return self.get_sensors_data()
        elif self.path == self.server_class.path.CONFIG_ETH:
            return self.get_ethernet_config()
        elif self.path == self.server_class.path.CONFIG_WIFI:
            return self.get_wifi_config()
        elif self.path == self.server_class.path.CONFIG_LTE:
            return self.get_lte_config()
        elif self.path == self.server_class.path.CONFIG_MQTT:
            return self.get_mqtt_data()
        elif self.path == self.server_class.path.CONFIG_SENSORS:
            pass

        return self.default_response()

    def do_POST(self):
        logging.info(f"POST request received for: {self.path}")
        # --- Handle POST ---
        try:
            content_length = int(self.headers['Content-Length'])
            post_body_bytes = self.rfile.read(content_length)
            post_body_string = post_body_bytes.decode('utf-8')
            data = json.loads(post_body_string)
        except json.JSONDecodeError as e:
            logging.error(f"Error decoding JSON from POST request: {e}")
            return {'status': 400}
        if self.path == self.server_class.path.SENSORS_DATA:
            return self.post_sensors_data(self, data)
        elif self.path == self.server_class.path.CONFIG_MQTT:
            return self.post_mqtt_data(self, data)
        elif self.path == self.server_class.path.CONFIG_ETH:
            return self.post_ethernet_config(self, data)
        elif self.path == self.server_class.path.CONFIG_WIFI:
            return self.post_wifi_data(self, data)
        elif self.path == self.server_class.path.CONFIG_LTE:
            return self.post_lte_data(self, data)
        elif self.path == self.server_class.path.CONFIG_SENSORS:
            pass

        return self.default_response()

    def do_OPTIONS(self):
        # Handle preflight CORS requests
        self.send_response(200)
        self._set_headers()
        self.end_headers()

    def set_json_headers(self, http_code, success_response=None) -> None:
        self.send_response(http_code)

        self._set_headers()   
        self.send_header("Content-type", "application/json")
        self.end_headers()

    def default_response(self) -> None:
        """
        Implementation for default server response.
        """
        response = self.server_class.response.DEFAULT_RESPONSE
        self.set_json_headers(404, response)
        self.wfile.write(json.dumps(response).encode('utf-8'))

    def get_sensors_data(self) -> None:
        """
        Build the response for sensor GET command
        """
        response = sensor_data.get_sensor_data()
        self.set_json_headers(200, response)
        self.wfile.write(json.dumps(response).encode('utf-8'))

    def get_mqtt_data(self) -> None:
        """
        Build the response for mqtt GET command
        """
        response = mqtt_data.get_mqtt_data()
        self.set_json_headers(200, response)
        self.wfile.write(json.dumps(response).encode('utf-8'))

    def get_ethernet_config(self) -> None:
        """
        Build the response for ethernet GET command
        """
        response = ethernet_data.get_ethernet()
        response["status"] = 200
        self.set_json_headers(200, response)
        self.wfile.write(json.dumps(response).encode('utf-8'))

    def get_wifi_config(self) -> None:
        """
        Build the response for ethernet GET command
        """
        response = netif.WiFiIface("enps0").get_interface_info()
        response["status"] = 200
        self.set_json_headers(200, response)
        self.wfile.write(json.dumps(response).encode('utf-8'))

    def get_lte_config(self) -> None:
        """
        Build the response for ethernet GET command
        """
        response = netif.LTEIface("ppp0").get_interface_info()
        response["status"] = 200
        self.set_json_headers(200, response)
        self.wfile.write(json.dumps(response).encode('utf-8'))

    def status_network_response(self) -> None:
        response = self.server_class.response.INIT_JSON_STATUS_NETWORK_DATA
        response["ethernet"] = netif.EthernetIface("eth1").get_interface_info()
        response["wifi"] = netif.WiFiIface("enps0").get_interface_info()
        response["lte"] = netif.LTEIface("ppp0").get_interface_info()

        self.set_json_headers(200, response)
        self.wfile.write(json.dumps(response).encode('utf-8'))

    def post_sensors_data(self, data) -> None:
        """
        Build the response for sensor GET command
        """
        response = sensor_data.post_sensor(data)
        self.set_json_headers(200, response)
        self.wfile.write(json.dumps(response).encode('utf-8'))

    def post_mqtt_data(self, data) -> None:
        """
        Build the response for mqtt GET command
        """
        response = mqtt_data.post_mqtt(data)
        self.set_json_headers(200, response)
        self.wfile.write(json.dumps(response).encode('utf-8'))

    def post_ethernet_config(self) -> None:
        """
        Build the response for ethernet GET command
        """
        response = ethernet_data.post_ethernet(self)
        self.set_json_headers(response['status'], response)
        self.wfile.write(json.dumps(response).encode('utf-8'))

    def post_wifi_config(self) -> None:
        """
        Build the response for wifi GET command
        """
        response = wifi_data.post_wifi(self)
        self.set_json_headers(response['status'], response)
        self.wfile.write(json.dumps(response).encode('utf-8'))

    def post_lte_config(self) -> None:
        """
        Build the response for lte GET command
        """
        response = lte_data.post_lte(self)
        self.set_json_headers(response['status'], response)
        self.wfile.write(json.dumps(response).encode('utf-8'))
