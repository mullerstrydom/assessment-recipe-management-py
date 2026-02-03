import logging

from sqlmodel import select

from recipe_management.services.dto.recipe_dto import RecipeDto
from recipe_management.data.ingredient import Ingredient
from recipe_management.data.recipe import Recipe
from recipe_management.data.recipe_ingredient_map import RecipeIngredientMap
from recipe_management.data.recipe_repository import RecipeRepository
from recipe_management.services.ingredient_service import IngredientService


class RecipeService:
    def __init__(self, repository: RecipeRepository, ingredient_service: IngredientService):
        self.repository = repository
        self.ingredient_service = ingredient_service

    def get_all_recipes(self, is_vegetarian: bool | None = None,
                        number_of_servings: int | None = None,
                        include_ingredients: list[str] | None = None,
                        exclude_ingredients: list[str] | None = None,
                        search: str | None = None) -> list[RecipeDto]:
        """
        Find all recipes matching the given criteria.
        :param is_vegetarian: boolean indicating if only vegetarian recipes should be returned
        :param number_of_servings: number of servings
        :param include_ingredients: ingredient names to include
        :param exclude_ingredients: ingredient names to exclude
        :param search: text to search in the instructions
        :return: list of RecipeDto
        """

        sql = (select(Recipe).outerjoin(RecipeIngredientMap)).outerjoin(Ingredient)
        if is_vegetarian is not None:
            subquery_non_vegetarian_recipes = select(RecipeIngredientMap.recipe_id).join(Ingredient).where(Ingredient.is_vegetarian == False)
            if is_vegetarian:
                sql = sql.where(Recipe.id.notin_(subquery_non_vegetarian_recipes))
            else:
                sql = sql.where(Recipe.id.in_(subquery_non_vegetarian_recipes))

        if number_of_servings is not None:
            sql = sql.where(Recipe.number_of_servings == number_of_servings)

        if include_ingredients is not None:
            sql = sql.where(Ingredient.name.in_(include_ingredients))

        if exclude_ingredients is not None:
            subquery = select(RecipeIngredientMap.recipe_id).join(Ingredient).where(Ingredient.name.in_(exclude_ingredients))
            sql = sql.where(Recipe.id.notin_(subquery))

        if search is not None:
            sql = sql.where(Recipe.instructions.contains(search))

        rows: list[Recipe] = self.repository.get_advanced(sql.distinct())
        return [self._map_recipe_to_dto(recipe) for recipe in rows]

    def get_recipe_by_id(self, recipe_id: int) -> RecipeDto:
        return self._map_recipe_to_dto(self.repository.get_by_id(recipe_id))

    def create_recipe(self, recipe: RecipeDto) -> int:
        """
        Create a new recipe.
        :param recipe: recipe dto
        :return: id of created recipe
        """
        db_recipe = Recipe(name=recipe.recipeName,
                           number_of_servings=recipe.numberOfServings,
                           instructions=recipe.instructions)
        self.repository.save(db_recipe)
        logging.debug("Created recipe %s with id %s", db_recipe.name, db_recipe.id)
        self._create_recipe_ingredient_mappings(db_recipe.id, recipe.ingredients)
        return db_recipe.id

    def update_recipe(self, recipe_dto: RecipeDto) -> int:
        """
        Update an existing recipe.
        :param recipe_dto: recipe dto to update
        :return: id of recipe
        """
        recipe: Recipe = self.repository.get_by_id(recipe_dto.id)
        if not recipe:
            raise Exception(f"Recipe with id {recipe_dto.id} not found")
        recipe.name = recipe_dto.recipeName
        recipe.number_of_servings = recipe_dto.numberOfServings
        recipe.instructions = recipe_dto.instructions
        self.repository.save(recipe)

        self.repository.delete_ingredient_map(recipe.id)
        self._create_recipe_ingredient_mappings(recipe.id, recipe_dto.ingredients)
        return recipe.id

    def delete_recipe(self, recipe_id: int) -> None:
        """
        Delete a recipe by its id.
        :param recipe_id: id of recipe
        :return: None
        """
        recipe: Recipe = self.repository.get_by_id(recipe_id)
        if not recipe:
            raise Exception(f"Recipe with id {recipe_id} not found")

        self.repository.delete_ingredient_map(recipe.id)
        self.repository.delete_by_id(recipe.id)

    def _create_recipe_ingredient_mappings(self, recipe_id: int, ingredient_names: list[str]):
        """
        Create mappings between a recipe and its ingredients.
        :param recipe_id: id of recipe
        :param ingredient_names: list of ingredient names
        """
        for ingredient_name in ingredient_names:
            ingredient = self.ingredient_service.find_or_create(ingredient_name)
            recipe_ingredient_map = RecipeIngredientMap(recipe_id=recipe_id, ingredient_id=ingredient.id)
            self.repository.create_ingredient_map(recipe_ingredient_map)

    def _map_recipe_to_dto(self, recipe: Recipe) -> RecipeDto:
        rows = self.ingredient_service.find_names_by_recipe(recipe.id)
        ingredient_names = [row for row in rows]

        return RecipeDto(id=recipe.id,
                         recipeName=recipe.name,
                         ingredients=ingredient_names,
                         numberOfServings=recipe.number_of_servings,
                         instructions=recipe.instructions)