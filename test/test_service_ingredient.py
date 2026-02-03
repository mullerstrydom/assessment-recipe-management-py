from argparse import Namespace
from unittest import TestCase

from sqlalchemy import func
from sqlmodel import select, col

from recipe_management.data.ingredient import Ingredient
from recipe_management.data.ingredient_repository import IngredientRepository
from recipe_management.data.recipe import Recipe
from recipe_management.data.recipe_ingredient_map import RecipeIngredientMap
from recipe_management.data.sqlite_connection import SqliteDatabase
from recipe_management.services.ingredient_info_service import IngredientInfoService
from recipe_management.services.ingredient_service import IngredientService

commandline_arguments: Namespace = Namespace(
    db_url="sqlite:///:memory:"
)


def get_session(database: SqliteDatabase):
    with database.get_session() as session:
        return session


class TestIngredientService(TestCase):

    def setUp(self):
        self.database = SqliteDatabase(commandline_arguments)
        self.session = get_session(self.database)
        self.repository = IngredientRepository(self.session)
        self.service = IngredientService(self.repository, IngredientInfoService())

    def tearDown(self):
        self.session.close()
        self.database.close()

    def test_find_or_create__existing_ingredient(self):
        # given
        ingredient_name = "Tomato"
        ingredient = Ingredient(name=ingredient_name, is_vegetarian=True)
        self.repository.save(ingredient)

        count_before = self.session.exec(select(func.count(col(Ingredient.id)))).one()

        # when
        ingredient = self.service.find_or_create(ingredient_name)
        count_after = self.session.exec(select(func.count(col(Ingredient.id)))).one()

        # then
        self.assertIsNotNone(ingredient)
        self.assertEqual(ingredient_name, ingredient.name)
        self.assertEqual(count_before, count_after, "No new ingredient should be created")

    def test_find_or_create__not_existing_ingredient(self):
        # given
        ingredient_name = "Tomato"
        count_before = self.session.exec(select(func.count(col(Ingredient.id)))).one()

        # when
        ingredient = self.service.find_or_create(ingredient_name)
        count_after = self.session.exec(select(func.count(col(Ingredient.id)))).one()

        # then
        self.assertEqual(0, count_before, "No ingredients should be in the table")
        self.assertEqual(1, count_after, "New ingredient should be created")
        self.assertIsNotNone(ingredient)
        self.assertEqual(ingredient_name, ingredient.name)

    def test_find_names_by_recipe(self):
        # given
        recipe = Recipe(name="Test Recipe", number_of_services=4, instructions="Test Instructions")
        ingredient1 = Ingredient(name="Tomato", is_vegetarian=True)
        ingredient2 = Ingredient(name="Bacon", is_vegetarian=True)
        ingredient3 = Ingredient(name="Cheese", is_vegetarian=True)
        ingredient4 = Ingredient(name="Milk", is_vegetarian=True)
        self.session.add(recipe)
        self.session.add(ingredient1)
        self.session.add(ingredient2)
        self.session.add(ingredient3)
        self.session.add(ingredient4)
        self.session.commit()
        self.session.refresh(recipe)
        self.session.refresh(ingredient1)
        self.session.refresh(ingredient2)
        ri_map1 = RecipeIngredientMap(recipe_id=recipe.id, ingredient_id=ingredient1.id)
        ri_map2 = RecipeIngredientMap(recipe_id=recipe.id, ingredient_id=ingredient2.id)
        self.session.add(ri_map1)
        self.session.add(ri_map2)
        self.session.commit()

        recipe_id = recipe.id

        # when
        ingredient_names = self.service.find_names_by_recipe(recipe_id)

        # then
        self.assertEqual(2, len(ingredient_names), "There should be two ingredients for the recipe")
        self.assertIn("Tomato", ingredient_names)
        self.assertIn("Bacon", ingredient_names)