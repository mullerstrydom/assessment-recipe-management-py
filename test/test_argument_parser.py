import sys
from io import StringIO
from unittest import TestCase

from recipe_management.arguments.argument_parser import ArgumentParser
from recipe_management.main import StartPhase


class ApplicationHelpTest(TestCase):

    def test_help(self):
        expected_output = """usage: app.py [-h] --log-file-name LOG_FILE_NAME
              [--log-level {DEBUG,INFO,WARN,ERROR}]
              [--log-file-size LOG_FILE_SIZE]
              [--log-backup-count LOG_BACKUP_COUNT]
              [--http-address HTTP_ADDRESS] [--http-port HTTP_PORT]
              [--db-url DB_URL]

Recipe management

options:
  -h, --help            show this help message and exit
  --log-file-name LOG_FILE_NAME
                        Log file name
  --log-level {DEBUG,INFO,WARN,ERROR}
                        Log level name
  --log-file-size LOG_FILE_SIZE
                        File size of each log file in MB
  --log-backup-count LOG_BACKUP_COUNT
                        Number of backup log files to keep
  --http-address HTTP_ADDRESS
                        The address of the HTTP server
  --http-port HTTP_PORT
                        The port of the HTTP server
  --db-url DB_URL       The address of the database server
"""

        # given
        old_stdout = sys.stdout
        temp_stdout = StringIO()
        # when
        try:
            sys.stdout = temp_stdout
            sys.argv = ["app.py", "--help"]

            argument_parser = ArgumentParser(description="Recipe management",
                                             list_of_arguments=StartPhase.list_of_arguments)
            argument_parser.parse()

        except (Exception, SystemExit):
            output = temp_stdout.getvalue()
            #then
            self.assertEqual(expected_output, output)

        finally:
            sys.stdout = old_stdout
