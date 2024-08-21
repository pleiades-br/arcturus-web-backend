from http.server import HTTPServer
from http_handler import SimpleHandler
import argparse


def run(server_class=HTTPServer, handler_class=SimpleHandler, port=8080):
    server_address = ('127.0.0.1', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

def main():
    '''
        Argument parsing with argparse and main job
    '''
    parser = argparse.ArgumentParser(description='Prove of concept for Arcturus project')
    parser.add_argument('--port', type=int, default=8080, help='Port that service will connect')
    args = parser.parse_args()
    run(port=args.port)


if __name__ == '__main__':
    main()