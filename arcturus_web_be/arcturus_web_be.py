from http.server import HTTPServer
from http_handler import SimpleHandler
import argparse


def start_server(server_class=HTTPServer, handler_class=SimpleHandler, addr="127.0.0.1", port=8080):
    server_address = (addr, port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

def main():
    '''
        Argument parsing with argparse and main job
    '''
    parser = argparse.ArgumentParser(description="Arcturus backend Service")
    parser.add_argument(
        "-l",
        "--listen-addr",
        type=str, 
        default="127.0.0.1",
        help="IP Address to listen, string format (Default: 127.0.0.1)"
    )

    parser.add_argument(
        "-p",
        "--port",
        type=int, 
        default=8080, 
        help='Port to listen, integer format (Default: 8080)'
    )

    args = parser.parse_args()
    start_server(addr=args.listen_addr, port=args.port)


if __name__ == '__main__':
    main()