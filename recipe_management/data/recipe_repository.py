from sqlalchemy import Select
from sqlmodel import Session, select

from recipe_management.data.recipe import Recipe
from recipe_management.data.recipe_ingredient_map import RecipeIngredientMap


class RecipeRepository:

    def __init__(self, session: Session):
        self.session = session

    def save(self, recipe: Recipe) -> Recipe:
        self.session.add(recipe)
        self.session.commit()
        self.session.refresh(recipe)
        return recipe

    def get_by_id(self, recipe_id: int) -> Recipe | None:
        return self.session.get(Recipe, recipe_id)

    def get_advanced(self, sql: Select) -> list[Recipe]:
        results = self.session.exec(sql).all()
        return [recipe for recipe in results]

    def delete_by_id(self, recipe_id: int) -> Recipe:
        recipe = self.get_by_id(recipe_id)
        if recipe:
            self.session.delete(recipe)
            self.session.commit()
        return recipe

    def delete_ingredient_map(self, recipe_id: int):
        all_mappings = self.session.exec(select(RecipeIngredientMap).where(RecipeIngredientMap.recipe_id == recipe_id)).all()
        for ingredient_map in all_mappings:
            self.session.delete(ingredient_map)
        self.session.commit()

    def create_ingredient_map(self, recipe_ingredient_map: RecipeIngredientMap) -> RecipeIngredientMap:
        self.session.add(recipe_ingredient_map)
        self.session.commit()
        self.session.refresh(recipe_ingredient_map)
        return recipe_ingredient_map