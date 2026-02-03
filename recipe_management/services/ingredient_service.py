import logging

from sqlmodel import select

from recipe_management.data.ingredient_repository import IngredientRepository
from recipe_management.data.ingredient import Ingredient
from recipe_management.data.recipe_ingredient_map import RecipeIngredientMap
from recipe_management.services.ingredient_info_service import IngredientInfoService


class IngredientService:

    def __init__(self, repository: IngredientRepository, ingredient_info_service: IngredientInfoService):
        self.repository = repository
        self.ingredient_info_service = ingredient_info_service

    def find_by_name(self, name: str):
        return self.repository.get_ingredient(name)

    def create_ingredient(self, name: str) -> Ingredient:
        is_vegetarian: bool = self.ingredient_info_service.is_vegetarian(name)
        ingredient = Ingredient(name=name, is_vegetarian=is_vegetarian)
        self.repository.save(ingredient)
        logging.debug("Created ingredient %s with id %d", name, ingredient.id)
        return ingredient

    def find_or_create(self, name) -> Ingredient:
        ingredient = self.find_by_name(name)
        if ingredient is None:
            ingredient = self.create_ingredient(name)
        return ingredient

    def find_names_by_recipe(self, recipe_id: int) -> list[str]:
        sql = select(Ingredient).join(RecipeIngredientMap).where(RecipeIngredientMap.recipe_id == recipe_id)
        ingredients: list[Ingredient] = self.repository.get_advanced(sql)
        return [ingredient.name for ingredient in ingredients]