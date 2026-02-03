import enum
import logging
from argparse import ArgumentParser


class Levels(int, enum.Enum):
    DEBUG = logging.DEBUG,
    INFO = logging.INFO,
    WARN = logging.WARNING,
    ERROR = logging.ERROR


class LoggerArgument:

    def __init__(self, log_level="INFO", log_file_size=5, backup_count=3):
        self.log_level = log_level
        self.log_file_size = log_file_size
        self.backup_count = backup_count

    def parse(self, argument_parser: ArgumentParser):
        argument_parser.add_argument('--log-file-name',
                                     help='Log file name',
                                     required=True)
        argument_parser.add_argument('--log-level',
                                     help='Log level name',
                                     choices=[level.name for level in Levels],
                                     default=self.log_level)
        argument_parser.add_argument('--log-file-size',
                                     help='File size of each log file in MB',
                                     default=self.log_file_size)
        argument_parser.add_argument('--log-backup-count',
                                     help='Number of backup log files to keep',
                                     default=self.backup_count)
