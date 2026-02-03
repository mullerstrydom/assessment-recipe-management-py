from sqlmodel import SQLModel, Field


class Ingredient(SQLModel, table=True):
    __tablename__ = "ingredients"
    id: int = Field(default=None, primary_key=True)
    name: str = Field(default=None, unique=True)
    is_vegetarian: bool = Field(default=False, nullable=False)