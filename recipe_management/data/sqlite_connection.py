import logging
from contextlib import contextmanager

from sqlalchemy import create_engine, StaticPool
from sqlmodel import SQLModel, Session

from recipe_management.data.database_connection import IDatabaseConnection
from recipe_management.data.ingredient import Ingredient
from recipe_management.data.recipe import Recipe
from recipe_management.data.recipe_ingredient_map import RecipeIngredientMap


def get_url_from_arguments(commandline_arguments) -> str:
    """
    Get the database url from the commandline arguments
    If the url is for an in-memory sqlite database, ensure that the database is persistent across connections
    :param commandline_arguments: Namespace
    :return: str
    """
    url = commandline_arguments.db_url
    if url.startswith("sqlite:///:memory:"):
        SqliteDatabase.poolClass = StaticPool
    return url


class SqliteDatabase(IDatabaseConnection):
    poolClass = None

    def __init__(self, commandline_arguments):
        IDatabaseConnection.__init__(self)
        self.url = get_url_from_arguments(commandline_arguments)
        self.engine = create_engine(self.url, connect_args={"check_same_thread": False}, poolclass=SqliteDatabase.poolClass)
        self.create_tables()

    def create_tables(self):
        assert Recipe
        assert Ingredient
        assert RecipeIngredientMap
        SQLModel.metadata.create_all(self.engine)

    @contextmanager
    def get_session(self):
        with Session(self.engine) as session:
            logging.debug("DatabaseConnection.get_session()")
            yield session

    def close(self):
        self.engine.dispose()