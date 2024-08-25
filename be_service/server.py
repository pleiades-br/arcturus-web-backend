from http.server import HTTPServer
from http_handler import SimpleHandler
from json import dumps, loads


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
    INIT_JSON_STATUS_NETWORK_DATA = {"status": True, "ethernet": {}, "wifi": {}, "lte": {}}


class Storage():
    def __init__(self, response_data) -> None:
        self.response_data = response_data
        self.json = ""

    def write_json(self, data) -> None:
        self.json = data

    def read_json(self) -> str:
        return self.json
    


class RequestHandler(SimpleHandler):
    def __init__(self, request, client_address, server_class) -> None:
        super().__init__(request, client_address, server_class)
        self.server_class = server_class

    def do_GET(self):
        pass

    def do_POST(self):
        pass

    def set_json_headers(self, success_response=None):
        self.send_response(200)
        if success_response is not None:
            self.send_header("Content-type", "application/json")
            self.send_header("Content-Length", str(len(success_response)))
        self.end_headers()



class Server(HTTPServer):
    def __init__(self, server_address, request_handler, storage, paths, response) -> None:
        super().__init__(server_address, request_handler)
        self.storage = storage
        self.path = paths
        self.response = response