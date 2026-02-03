from argparse import Namespace
from unittest import TestCase

from sqlalchemy import func
from sqlmodel import select, col

from recipe_management.data.ingredient import Ingredient
from recipe_management.data.ingredient_repository import IngredientRepository
from recipe_management.data.sqlite_connection import SqliteDatabase


commandline_arguments: Namespace = Namespace(
    db_url="sqlite:///:memory:"
)

def get_session(database: SqliteDatabase):
    with database.get_session() as session:
        return session


class TestIngredientsRepositories(TestCase):

    def setUp(self):
        self.database = SqliteDatabase(commandline_arguments)
        self.session = get_session(self.database)
        self.ingredient_repository = IngredientRepository(self.session)

    def tearDown(self):
        self.database.close()

    def test_ingredient_save(self):
        # given
        ingredient: Ingredient = Ingredient(
            name="Test Ingredient",
            is_vegetarian=True,
        )
        count_before = self.session.exec(select(func.count(col(Ingredient.id)))).one()

        # when
        self.ingredient_repository.save(ingredient)

        # then
        count_after = self.session.exec(select(func.count(col(Ingredient.id)))).one()
        self.assertEqual(0, count_before, "There should be no ingredients before the test")
        self.assertEqual(1, count_after, "There should be one ingredient after the test")
        self.assertIsNotNone(ingredient.id, "The ingredient ID should be set after saving")

    def test_ingredient_get(self):
        # given
        ingredient: Ingredient = Ingredient(
            name="Test Ingredient",
            is_vegetarian=True,
        )
        self.session.add(ingredient)
        self.session.commit()

        # when
        founded_ingredient = self.ingredient_repository.get_ingredient("Test Ingredient")

        # then
        self.assertEqual(ingredient.name, founded_ingredient.name, "The ingredient name should match")
        self.assertEqual(ingredient.is_vegetarian, founded_ingredient.is_vegetarian, "The ingredient name should match")

    def test_ingredient_get_advanced(self):
        # given
        ingredient: Ingredient = Ingredient(
            name="Test Ingredient",
            is_vegetarian=True,
        )
        self.session.add(ingredient)
        self.session.commit()

        # when
        sql = select(Ingredient)
        list_of_ingredients: list[Ingredient] = self.ingredient_repository.get_advanced(sql)

        # then
        self.assertEqual(1, len(list_of_ingredients), "There should be one ingredient in the list, and sql correctly executed")
