from typing import Any, AsyncGenerator, Annotated

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from sqlmodel import Session

from recipe_management.data.ingredient_repository import IngredientRepository
from recipe_management.data.recipe_repository import RecipeRepository
from recipe_management.data.sqlite_connection import IDatabaseConnection
from recipe_management.services.ingredient_info_service import IngredientInfoService
from recipe_management.services.ingredient_service import IngredientService
from recipe_management.services.recipe_service import RecipeService

database_connection: IDatabaseConnection | None = None

def set_database_for_dependencies(db_connection: IDatabaseConnection):
    global database_connection
    database_connection = db_connection


async def get_db() -> AsyncGenerator[Session, Any]:
    with database_connection.get_session() as session:
        yield session

def get_ingredient_repository(db=Depends(get_db)):
    return IngredientRepository(db)

def get_recipe_repository(db=Depends(get_db)):
    return RecipeRepository(db)

def get_ingredient_info_service() -> IngredientInfoService:
    return IngredientInfoService()


def get_ingredient_service(repository: IngredientRepository = Depends(get_ingredient_repository),
                           ingredient_info_service: IngredientInfoService = Depends(get_ingredient_info_service)) -> IngredientService:
    return IngredientService(repository, ingredient_info_service)


def get_recipe_service(repository: RecipeRepository = Depends(get_recipe_repository),
                       ingredient_service: IngredientService = Depends(get_ingredient_service)) -> RecipeService:
    return RecipeService(repository, ingredient_service)

def authorized_user(credentials: Annotated[HTTPBasicCredentials, Depends(HTTPBasic())]):
    # Placeholder for actual authentication logic
    if credentials.username == "demo" and credentials.password == "demo":
        return credentials.username
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")