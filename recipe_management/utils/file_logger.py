import logging
import os
from contextlib import contextmanager
from logging.handlers import RotatingFileHandler
from pathlib import Path

import recipe_management
from recipe_management.arguments.logger_argument import Levels


class FileLogger:
    FORMAT = '%(asctime)s [%(levelname)s] - %(message)s'
    DATEFMT = '%Y-%m-%d %H:%M:%S'

    def __init__(self, commandline_arguments):
        self.log_file_name = commandline_arguments.log_file_name
        self.log_level = commandline_arguments.log_level
        self.log_file_size = commandline_arguments.log_file_size
        self.log_backup_count = commandline_arguments.log_backup_count

    @contextmanager
    def build(self):
        log_formatter = logging.Formatter(FileLogger.FORMAT, datefmt=FileLogger.DATEFMT)
        file = os.path.join(Path(recipe_management.__file__).parent.parent.absolute(), self.log_file_name + '.log')
        size = int(self.log_file_size) * 1024 * 1024
        level = Levels[self.log_level].value

        handler = RotatingFileHandler(file, mode='a', maxBytes=size, backupCount=self.log_backup_count)
        handler.setFormatter(log_formatter)
        handler.setLevel(level)

        logging.basicConfig(level=level,
                            format='%(asctime)s [%(levelname)s] - %(message)s',
                            datefmt='%Y%m%d %H:%M:%S',
                            handlers=[handler]
                            )
        yield