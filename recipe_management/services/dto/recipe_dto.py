from pydantic import BaseModel


class RecipeDto(BaseModel):
    id: int | None = None
    recipeName: str
    numberOfServings: int
    ingredients: list[str]
    instructions: str
