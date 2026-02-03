from argparse import Namespace
from unittest import TestCase

from sqlalchemy import Row
from sqlmodel import select
from starlette.testclient import TestClient

from recipe_management.data.ingredient import Ingredient
from recipe_management.data.recipe import Recipe
from recipe_management.data.recipe_ingredient_map import RecipeIngredientMap
from recipe_management.data.sqlite_connection import IDatabaseConnection, SqliteDatabase
from recipe_management.main import MainPhase

commandline_arguments: Namespace = Namespace(
    db_url="sqlite:///:memory:",
    http_address="localhost",
    http_port=8000,
    log_level="DEBUG"
)


class IntegrationTest(TestCase):

    def setUp(self):
        self.database_connection = SqliteDatabase(commandline_arguments)
        main_phase = MainPhase(commandline_arguments, self.database_connection)

        self.rest_client = TestClient(main_phase.rest_api.app, headers={"Authorization": "Basic ZGVtbzpkZW1v"})  # demo:demo base64 encoded

    def tearDown(self):
        self.database_connection.close()

    def test_get_all(self):
        # given
        setup_data(self.database_connection)

        # when
        response = self.rest_client.get("/recipes")

        # then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [
            {
                'id': 100,
                'ingredients': ['Ingredient1'],
                'instructions': 'Mix ingredients.',
                'numberOfServings': 1,
                'recipeName': 'Recipe1'
            },
            {
                'id': 101,
                'ingredients': ['Ingredient1', 'Ingredient2'],
                'instructions': 'Mix ingredients.',
                'numberOfServings': 2,
                'recipeName': 'Recipe2'
            }
        ])

    def test_get_only_vegetarian(self):
        # given
        setup_data(self.database_connection)

        # when
        response = self.rest_client.get("/recipes?isVegetarian=true")

        # then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [
            {
                'id': 100,
                'ingredients': ['Ingredient1'],
                'instructions': 'Mix ingredients.',
                'numberOfServings': 1,
                'recipeName': 'Recipe1'
            }
        ])

    def test_get_by_number_of_servings(self):
        # given
        setup_data(self.database_connection)

        # when
        response = self.rest_client.get("/recipes?numberOfServings=1")

        # then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [
            {
                'id': 100,
                'ingredients': ['Ingredient1'],
                'instructions': 'Mix ingredients.',
                'numberOfServings': 1,
                'recipeName': 'Recipe1'
            }
        ])

    def test_post_create_recipe(self):
        # given
        json = {
            'ingredients': ['Ingredient1'],
            'instructions': 'Mix ingredients.',
            'numberOfServings': 1,
            'recipeName': 'Recipe1'
        }

        # when
        response = self.rest_client.post("/recipes", json=json)

        # then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'1')

        with self.database_connection.get_session() as session:
            db_recipe: Row = session.execute(select(Recipe).where(Recipe.id == 1)).scalars().first()
            self.assertEqual('Recipe1', db_recipe.name)
            self.assertEqual("Mix ingredients.", db_recipe.instructions)
            self.assertEqual(1, db_recipe.number_of_servings)

            db_ingredient: Ingredient = session.execute(select(Ingredient).where(Ingredient.id == 1)).scalars().first()
            self.assertEqual('Ingredient1', db_ingredient.name)
            self.assertTrue(db_ingredient.is_vegetarian)

            db_ri_map: RecipeIngredientMap = session.execute(select(RecipeIngredientMap).where(
                RecipeIngredientMap.recipe_id == 1 and RecipeIngredientMap.ingredient_id == 1)).scalars().first()
            self.assertIsNotNone(db_ri_map)

    def test_put_update_recipe(self):
        # given
        setup_data(self.database_connection)
        json = {
            'id': 100,
            'ingredients': ['Ingredient1'],
            'instructions': 'Mix ingredients.',
            'numberOfServings': 1,
            'recipeName': 'New recipe name'
        }

        # when
        response = self.rest_client.put("/recipes", json=json)

        # then
        self.assertEqual(response.status_code, 200)
        with self.database_connection.get_session() as session:
            row = session.execute(select(Recipe.name).where(Recipe.id == 100)).first()
            self.assertEqual("New recipe name", row[0])

    def test_delete_recipe(self):
        # given
        setup_data(self.database_connection)

        # when
        response = self.rest_client.delete("/recipes/100")

        # then
        self.assertEqual(response.status_code, 200)
        with self.database_connection.get_session() as session:
            row = session.execute(select(Recipe).where(Recipe.id == 100)).first()
            self.assertIsNone(row)

def setup_data(database_connection: IDatabaseConnection):
    recipe1: Recipe = Recipe(id=100, name="Recipe1", number_of_servings=1, instructions="Mix ingredients.")
    recipe2: Recipe = Recipe(id=101, name="Recipe2", number_of_servings=2, instructions="Mix ingredients.")
    ingredient1: Ingredient = Ingredient(id=200, name="Ingredient1", is_vegetarian=True)
    ingredient2: Ingredient = Ingredient(id=201, name="Ingredient2", is_vegetarian=False)
    ri_map_1: RecipeIngredientMap = RecipeIngredientMap(recipe_id=100, ingredient_id=200)
    ri_map_2: RecipeIngredientMap = RecipeIngredientMap(recipe_id=101, ingredient_id=200)
    ri_map_3: RecipeIngredientMap = RecipeIngredientMap(recipe_id=101, ingredient_id=201)

    with database_connection.get_session() as session:
        session.add(recipe1)
        session.add(recipe2)
        session.add(ingredient1)
        session.add(ingredient2)
        session.add(ri_map_1)
        session.add(ri_map_2)
        session.add(ri_map_3)
        session.commit()
