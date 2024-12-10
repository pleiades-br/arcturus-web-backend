from http.server import HTTPServer, BaseHTTPRequestHandler
#import network_ifaces as netif
import sensor_data 
import json


class Path():
    SENSORS_DATA = "/api/sensors_data"
    CONFIG_ETH = "/api/ethernet"
    CONFIG_WIFI = "/api/wifi"
    CONFIG_LTE = "/api/lte"
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
            return get_sensor_data()
        elif self.path  == self.server_class.path.CONFIG_ETH:
            pass
        elif self.path  == self.server_class.path.CONFIG_WIFI:
            pass
        elif self.path  == self.server_class.path.CONFIG_LTE:
            pass
        elif self.path  == self.server_class.path.CONFIG_SENSORS:
            pass

        return self.default_response()


    def do_POST(self):
        pass



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
        '''
        Implementation for default server response.
        ''' 
        response = self.server_class.response.DEFAULT_RESPONSE
        self.set_json_headers(404, response)
        self.wfile.write(json.dumps(response).encode('utf-8'))

    def get_sensors_data(self) -> None:
        response = sensor_data.get_sensor_data()
        self.set_json_headers(200, response)
        self.wfile.write(json.dumps(response).encode('utf-8'))
    
    def status_network_response(self) -> None:
        response = self.server_class.response.INIT_JSON_STATUS_NETWORK_DATA
        response["ethernet"] = netif.EthernetIface("eth1").get_interface_info()
        response["wifi"] = netif.WiFiIface("enps0").get_interface_info()
        response["lte"] = netif.LTEIface("ppp0").get_interface_info()
        
        self.set_json_headers(200, response)
        self.wfile.write(json.dumps(response).encode('utf-8'))



