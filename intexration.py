import argparse
from intexration.server import Server

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-host', help='hostname', default='localhost')
    parser.add_argument('-port', help='port', default=8000)
    args = parser.parse_args()
    server = Server(host=args.host, port=args.port)
    server.start()

if __name__ == '__main__':
    main()