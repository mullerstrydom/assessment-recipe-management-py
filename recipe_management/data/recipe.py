from sqlmodel import SQLModel, Field


class Recipe(SQLModel, table=True):
    __tablename__ = "recipes"
    id: int = Field(default=None, primary_key=True)
    name: str = Field(default=None, unique=True, max_length=100)
    number_of_servings: int = Field(default=None, nullable=True)
    instructions: str = Field(default=None, nullable=True, max_length=4000)
