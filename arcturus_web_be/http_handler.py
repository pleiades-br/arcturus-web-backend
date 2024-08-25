from http.server import BaseHTTPRequestHandler
from network_ifaces import EthernetIface, LTEIface, WiFiIface
import json


class PathV1():
    STATUS_NETWORK = "/api/v1/status/network"

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        if self.path == '/api/v1/status/network':
            response = {"ethernet": EthernetIface("eth1").get_ipv4_info(),
                        "wifi": WiFiIface("wlan0").get_ipv4_info(),
                        "lte": LTEIface("ppp0").get_ipv6_info()}
        else:
            response = {"status": "path not found"}
        self.wfile.write(json.dumps(response).encode('utf-8'))

    def do_POST(self):
        return