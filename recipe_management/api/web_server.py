import logging

import uvicorn
from fastapi import FastAPI

from recipe_management.api.dependencies import set_database_for_dependencies
from recipe_management.api.recipe_router import router as recipe_router
from recipe_management.data.sqlite_connection import IDatabaseConnection


class WebServer:
    def __init__(self, commandline_arguments, database_connection: IDatabaseConnection):
        self.commandline_arguments = commandline_arguments
        self.database_connection = database_connection
        self.app = FastAPI()
        self.server = None
        self.setup()

    def setup(self):
        set_database_for_dependencies(self.database_connection)
        self.app.include_router(recipe_router)

    def start(self):
        self.server = uvicorn.Server(
            uvicorn.Config(self.app,
                           host=self.commandline_arguments.http_address,
                           port=self.commandline_arguments.http_port,
                           log_level="INFO"
                           )
        )
        logging.info(f"Web server started on {self.commandline_arguments.http_address}:{str(self.commandline_arguments.http_port)}")
        self.server.run()

    def stop(self):
        if self.server is not None:
            self.server.should_exit = True