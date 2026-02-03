from sqlmodel import SQLModel, Field


class RecipeIngredientMap(SQLModel, table=True):
    __tablename__ = "recipe_ingredient_map"
    id: int = Field(default=None, primary_key=True)
    recipe_id: int = Field(default=None, foreign_key='recipes.id')
    ingredient_id: int = Field(default=None, foreign_key='ingredients.id')