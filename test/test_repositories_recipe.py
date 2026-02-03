from argparse import Namespace
from unittest import TestCase

from sqlalchemy import func
from sqlmodel import select, col

from recipe_management.data.ingredient import Ingredient
from recipe_management.data.recipe import Recipe
from recipe_management.data.recipe_ingredient_map import RecipeIngredientMap
from recipe_management.data.recipe_repository import RecipeRepository
from recipe_management.data.sqlite_connection import SqliteDatabase


commandline_arguments: Namespace = Namespace(
    db_url="sqlite:///:memory:"
)

def get_session(database: SqliteDatabase):
    with database.get_session() as session:
        return session


class TestRecipeRepositories(TestCase):

    def setUp(self):
        self.database = SqliteDatabase(commandline_arguments)
        self.session = get_session(self.database)
        self.recipe_repository = RecipeRepository(self.session)

    def tearDown(self):
        self.database.close()

    def test_recipe_save(self):
        # given
        recipe: Recipe = Recipe(
            name="Test Recipe",
            description="This is a test recipe",
            instructions="1. Do something\n2. Do something else",
        )
        count_before = self.session.exec(select(func.count(col(Recipe.id)))).one()

        # when
        self.recipe_repository.save(recipe)

        # then
        count_after = self.session.exec(select(func.count(col(Recipe.id)))).one()
        self.assertEqual(0, count_before, "There should be no recipes before the test")
        self.assertEqual(1, count_after, "There should be one recipe after the test")
        self.assertIsNotNone(recipe.id, "The recipe ID should be set after saving")

    def test_recipe_get(self):
        # given
        recipe: Recipe = Recipe(
            name="Test Recipe",
            description="This is a test recipe",
            instructions="1. Do something\n2. Do something else",
        )
        self.session.add(recipe)
        self.session.commit()

        # when
        founded_recipe = self.recipe_repository.get_by_id(1)

        # then
        self.assertEqual(recipe.name, founded_recipe.name, "The recipe name should match")
        self.assertEqual(recipe.number_of_servings, founded_recipe.number_of_servings, "The recipe name should match")
        self.assertEqual(recipe.instructions, founded_recipe.instructions, "The recipe name should match")

    def test_recipe_get_advanced(self):
        # given
        recipe: Recipe = Recipe(
            name="Test Recipe",
            description="This is a test recipe",
            instructions="1. Do something\n2. Do something else",
        )
        self.session.add(recipe)
        self.session.commit()

        # when
        sql = select(Recipe)
        list_of_recipes: list[Recipe] = self.recipe_repository.get_advanced(sql)

        # then
        self.assertEqual(1, len(list_of_recipes), "There should be one recipe in the list, and sql correctly executed")

    def test_recipe_delete(self):
        # given
        recipe: Recipe = Recipe(
            name="Test Recipe",
            description="This is a test recipe",
            instructions="1. Do something\n2. Do something else",
        )
        self.session.add(recipe)
        self.session.commit()
        self.session.refresh(recipe)
        count_before = self.session.exec(select(func.count(col(Recipe.id)))).one()

        # when
        sql = select(Recipe)
        self.recipe_repository.delete_by_id(recipe.id)

        # then
        count_after = self.session.exec(select(func.count(col(Recipe.id)))).one()
        self.assertEqual(1, count_before, "There should be 1 recipe before the delete")
        self.assertEqual(0, count_after, "There should be 0 recipe after the delete")


    def test_recipe_ingredient_map_save(self):
        # given
        recipe: Recipe = Recipe(
            name="Test Recipe",
            description="This is a test recipe",
            instructions="1. Do something\n2. Do something else",
        )
        ingredient: Ingredient = Ingredient(
            name="Test Ingredient",
            is_vegetarian=True
        )
        self.session.add(recipe)
        self.session.add(ingredient)
        self.session.commit()
        self.session.refresh(recipe)
        self.session.refresh(ingredient)

        # when
        recipe_ingredient_map: RecipeIngredientMap = RecipeIngredientMap(
            recipe_id=recipe.id,
            ingredient_id=ingredient.id
        )
        self.recipe_repository.create_ingredient_map(recipe_ingredient_map)

        # then
        self.assertIsNotNone(recipe_ingredient_map.id, "The ID should be set after saving")

    def test_recipe_ingredient_map_delete(self):
        # given
        recipe: Recipe = Recipe(
            name="Test Recipe",
            description="This is a test recipe",
            instructions="1. Do something\n2. Do something else",
        )
        ingredient: Ingredient = Ingredient(
            name="Test Ingredient",
            is_vegetarian=True
        )
        self.session.add(recipe)
        self.session.add(ingredient)
        self.session.commit()
        self.session.refresh(recipe)
        self.session.refresh(ingredient)

        recipe_ingredient_map: RecipeIngredientMap = RecipeIngredientMap(
            recipe_id=recipe.id,
            ingredient_id=ingredient.id
        )
        self.session.add(recipe_ingredient_map)
        self.session.commit()
        self.session.refresh(recipe_ingredient_map)

        count_before = self.session.exec(select(func.count(col(RecipeIngredientMap.id)))).one()

        # when
        self.recipe_repository.delete_ingredient_map(recipe.id)

        # then
        count_after = self.session.exec(select(func.count(col(RecipeIngredientMap.id)))).one()
        self.assertEqual(1, count_before, "There should be 1 mapping before the delete")
        self.assertEqual(0, count_after, "There should be 0 mapping after the delete")