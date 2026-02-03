from sqlalchemy import Select
from sqlmodel import Session, select

from recipe_management.data.ingredient import Ingredient


class IngredientRepository:
    def __init__(self, session: Session):
        self.session = session

    def save(self, ingredient: Ingredient) -> Ingredient:
        self.session.add(ingredient)
        self.session.commit()
        self.session.refresh(ingredient)
        return ingredient

    def get_ingredient(self, name) -> Ingredient | None:
        sql = select(Ingredient).where(Ingredient.name == name)
        return self.session.exec(sql).first()

    def get_advanced(self, sql: Select) -> list[Ingredient]:
        results = self.session.exec(sql).all()
        return [ingredient for ingredient in results]