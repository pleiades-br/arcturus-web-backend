
import argparse
from server import Server, RequestHandler, Response, Path
import logging


def start_server(server_class=Server, handler_class=RequestHandler, addr="0.0.0.0", port=24042):
    server_address = (addr, port)
    http_server = server_class(server_address, handler_class, Path, Response)
    logging.debug(f"Starting server on {addr}:{port}")
    http_server.serve_forever()

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
        default=24042,
        help='Port to listen, integer format (Default: 24042)'
    )

    logging.basicConfig(level=logging.DEBUG, format="{levelname}: {message}", style="{")
    args = parser.parse_args()
    start_server(addr=args.listen_addr, port=args.port)


if __name__ == '__main__':
    main()