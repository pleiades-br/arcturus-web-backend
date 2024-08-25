from http.server import HTTPServer, BaseHTTPRequestHandler
import network_ifaces as netif
import json


class Path():
    STATUS_NETWORK = "/api/v1/status/network"
    STATUS_SENSORS = "/api/v1/status/sensors"
    CONFIG_ETH = "/api/v1/conf/ethernet"
    CONFIG_WIFI = "/api/v1/conf/wifi"
    CONFIG_LTE = "/api/v1/conf/lte"
    CONFIG_SENSORS = "/api/v1/conf/sensors"
    UTIL_SYSTEM_LOG = "/api/v1/util/log"
    UTIL_NETTOOLS = "/api/v1/util/nettools"
    UTIL_PAGE = "/api/v1/util/page"
    UTIL_BACKUP = "/api/v1/util/backup"
    UTIL_RESTORE = "/api/v1/util/restore"
    SEC_PASSWD = "/api/v1/sec/passwd"


class Response():
    DEFAULT_RESPONSE = {"status": False, "message": "No path found"}
    INIT_JSON_STATUS_NETWORK_DATA = {"status": True, "ethernet": {}, "wifi": {}, "lte": {}}


class Server(HTTPServer):
    def __init__(self, server_address, request_handler, paths, response) -> None:
        super().__init__(server_address, request_handler)
        self.path = paths
        self.response = response    


class RequestHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server_class) -> None:
        super().__init__(request, client_address, server_class)
        self.server_class = server_class

    def do_GET(self):
        if self.path == self.server_class.path.STATUS_NETWORK:
            pass
        elif self.path  == self.server_class.path.STATUS_SENSORS:
            pass

        return self.default_response()


    def do_POST(self):
        pass


    def set_json_headers(self, success_response=None) -> None:
        self.send_response(200)
        if success_response is not None:
            self.send_header("Content-type", "application/json")
            self.send_header("Content-Length", str(len(success_response)))
        self.end_headers()       


    def default_response(self) -> None:
        '''
        Implementation for default server response.
        ''' 
        response = self.server_class.response.DEFAULT_RESPONSE
        self.set_json_headers(response)
        self.wfile.write(json.dumps(response).encode('utf-8'))

    
    def status_network_response(self) -> None:
        response = self.server_class.response.INIT_JSON_STATUS_NETWORK_DATA
        response["ethernet"] = netif.EthernetIface("eth1").get_interface_info()
        response["wifi"] = netif.WiFiIface("enps0").get_interface_info()
        response["lte"] = netif.LTEIface("ppp0").get_interface_info()
        
        self.set_json_headers(response)
        self.wfile.write(json.dumps(response).encode('utf-8'))



