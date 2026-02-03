from argparse import Namespace
from unittest import TestCase
from unittest.mock import MagicMock

from recipe_management.data.ingredient import Ingredient
from recipe_management.data.recipe import Recipe
from recipe_management.data.recipe_repository import RecipeRepository
from recipe_management.data.sqlite_connection import SqliteDatabase
from recipe_management.services.dto.recipe_dto import RecipeDto
from recipe_management.services.ingredient_service import IngredientService
from recipe_management.services.recipe_service import RecipeService

commandline_arguments: Namespace = Namespace(
    db_url="sqlite:///:memory:"
)


def get_session(database: SqliteDatabase):
    with database.get_session() as session:
        return session


class TestRecipeService(TestCase):

    def setUp(self):
        self.database = SqliteDatabase(commandline_arguments)
        self.session = get_session(self.database)
        self.mock_repository = MagicMock(spec=RecipeRepository)
        self.mock_ingredient_service = MagicMock(spec=IngredientService)
        self.service = RecipeService(self.mock_repository, self.mock_ingredient_service)

    def tearDown(self):
        self.session.close()
        self.database.close()

    def test_get_all_recipes(self):
        # when
        self.service.get_all_recipes(None, None, None, None, None)

        # then
        self.mock_repository.get_advanced.assert_called_once()

    def test_create_recipe(self):
        # given
        dto = RecipeDto(recipeName="Test Recipe", numberOfServings=3, ingredients=["Tomato"], instructions="Do something")

        ingredient = Ingredient(id=1, name="Tomato", is_vegetarian=True)
        self.mock_ingredient_service.find_or_create.return_value = ingredient

        # when
        self.service.create_recipe(dto)

        # then
        self.mock_repository.save.assert_called_once_with(Recipe(name="Test Recipe", number_of_servings=3, instructions="Do something"))
        self.mock_ingredient_service.find_or_create.assert_called_once_with("Tomato")
        self.mock_repository.create_ingredient_map.assert_called_once()

    def test_update_recipe(self):
        # given
        dto = RecipeDto(id=1, recipeName="Updated Recipe", numberOfServings=4, ingredients=["Lettuce"], instructions="Do something else")

        existing_recipe = Recipe(id=1, name="Old Recipe", number_of_servings=2, instructions="Old instructions")
        self.mock_repository.get_by_id.return_value = existing_recipe

        ingredient = Ingredient(id=2, name="Lettuce", is_vegetarian=True)
        self.mock_ingredient_service.find_or_create.return_value = ingredient

        # when
        self.service.update_recipe(dto)

        # then
        self.mock_repository.save.assert_called_once_with(existing_recipe)
        self.mock_ingredient_service.find_or_create.assert_called_once_with("Lettuce")
        self.mock_repository.delete_ingredient_map.assert_called_once_with(1)
        self.mock_repository.create_ingredient_map.assert_called_once()

    def test_delete_recipe(self):
        # given
        existing_recipe = Recipe(id=1, name="Recipe to delete", number_of_servings=2, instructions="Some instructions")
        self.mock_repository.get_by_id.return_value = existing_recipe

        # when
        self.service.delete_recipe(1)

        # then
        self.mock_repository.delete_ingredient_map.assert_called_once_with(1)
        self.mock_repository.delete_by_id.assert_called_once_with(1)