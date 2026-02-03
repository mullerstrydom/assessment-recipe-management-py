from recipe_management import application_name
from recipe_management.api.web_server import WebServer
from recipe_management.arguments.argument_parser import ArgumentParser
from recipe_management.arguments.database_argument import DatabaseArgument
from recipe_management.arguments.http_argument import HttpArgument
from recipe_management.arguments.logger_argument import LoggerArgument
from recipe_management.data.sqlite_connection import SqliteDatabase, IDatabaseConnection
from recipe_management.utils.file_logger import FileLogger


class StartPhase:
    list_of_arguments = [
        LoggerArgument(),
        HttpArgument("0.0.0.0", 8000),
        DatabaseArgument()
    ]
    """
    Capture process arguments
    """
    def __init__(self):
        argument_parser = ArgumentParser(description=application_name, list_of_arguments=StartPhase.list_of_arguments)
        self.commandline_arguments = argument_parser.parse()

    def start(self):
        interface_phase = InterfacePhase(self.commandline_arguments)
        interface_phase.start()

class InterfacePhase:
    database_connection = None
    file_logger = None
    """
    Setup middleware connections such as database connection, and logging
    """

    def __init__(self, commandline_arguments):
        self.commandline_arguments = commandline_arguments
        self.database_connection: IDatabaseConnection = InterfacePhase.database_connection or SqliteDatabase(self.commandline_arguments)
        self.file_logger = InterfacePhase.file_logger or FileLogger(self.commandline_arguments)
        self.main_phase = None

    def start(self):
            with self.file_logger.build():
                self.main_phase = MainPhase(self.commandline_arguments, self.database_connection)
                try:
                    self.main_phase.start()
                except KeyboardInterrupt:
                    self.main_phase.stop()
                    self.database_connection.close()


class MainPhase:
    rest_api = None
    """
    Start the api server
    """
    def __init__(self, commandline_arguments, database_connection: IDatabaseConnection):
        self.rest_api = MainPhase.rest_api or WebServer(commandline_arguments, database_connection)

    def start(self):
        self.rest_api.start()

    def stop(self):
        self.rest_api.stop()


if __name__ == "__main__":
    startPhase = StartPhase()
    startPhase.start()