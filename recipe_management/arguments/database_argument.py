from argparse import ArgumentParser


class DatabaseArgument:

    def __init__(self):
        self.default_db_url = "sqlite:///:memory:"

    def parse(self, argument_parser: ArgumentParser):
        argument_parser.add_argument("--db-url",
                                     help="The address of the database server",
                                     type=str,
                                     default=self.default_db_url)