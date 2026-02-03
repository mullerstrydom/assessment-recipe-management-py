from argparse import ArgumentParser


class HttpArgument:
    def __init__(self, address: str, port: int):
        self.address = address
        self.port = port

    def parse(self, argument_parser: ArgumentParser):
        argument_parser.add_argument("--http-address",
                                     help="The address of the HTTP server",
                                     type=str,
                                     default=self.address)
        argument_parser.add_argument("--http-port",
                                     help="The port of the HTTP server",
                                     type=int,
                                     default=self.port)