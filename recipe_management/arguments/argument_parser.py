import argparse
import sys


class ArgumentParser:

    def __init__(self, description, list_of_arguments: list = None):
        self.parser = argparse.ArgumentParser(description=description,
                                              formatter_class=WidthRestrictedTextHelpFormatter)
        self._add_arguments(list_of_arguments)

    def _add_arguments(self, list_of_arguments=None):
        if list_of_arguments is not None:
            for argument in list_of_arguments:
                argument.parse(self.parser)

    def parse(self):
        sys.argv.pop(0)
        commandline_arguments = self.parser.parse_args(sys.argv)
        return commandline_arguments


class WidthRestrictedTextHelpFormatter(argparse.RawTextHelpFormatter):
    def __init__(self, prog: str):
        super().__init__(prog, width=80)