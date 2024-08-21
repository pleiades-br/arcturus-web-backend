from http.server import BaseHTTPRequestHandler
import json
import network_ifaces


class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        if self.path == '/api/v1/status/network':
            response = network_ifaces.get_ethenet_info()
        else:
            response = {"status": "path not found"}
        self.wfile.write(json.dumps(response).encode('utf-8'))

    def do_POST(self):
        return