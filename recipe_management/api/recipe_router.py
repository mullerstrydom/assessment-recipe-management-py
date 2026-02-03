from fastapi import APIRouter, Query
from fastapi.params import Depends

from recipe_management.api.dependencies import get_recipe_service
from recipe_management.services.dto.recipe_dto import RecipeDto
from recipe_management.services.recipe_service import RecipeService

router = APIRouter(
    prefix="/recipes",
    tags=["Recipe"],
)


# noinspection PyPep8Naming
# to keep query parameter naming consistent with the java implementation
@router.get("")
def get_all_recipes(isVegetarian: bool | None = Query(default=None, description="Filter for vegetarian recipes"),
                    numberOfServings: int | None = Query(default=None, description="Filter for recipes with specific number of servings"),
                    includeIngredients: list[str] | None = Query(default=None, description="Filter for recipes with specific ingredients"),
                    excludeIngredients: list[str] | None = Query(default=None, description="Filter for recipes without specific ingredients"),
                    search: str | None = Query(default=None, description="Search for recipes with specific instructions"),
                    recipe_service: RecipeService = Depends(get_recipe_service)) -> list[RecipeDto]:
    return recipe_service.get_all_recipes(isVegetarian, numberOfServings, includeIngredients, excludeIngredients, search)

@router.get("/{recipe_id}")
def get_recipe_by_id(recipe_id: int, recipe_service: RecipeService = Depends(get_recipe_service)) -> RecipeDto:
    return recipe_service.get_recipe_by_id(recipe_id)

@router.post("")
def create_recipe(recipe: RecipeDto, recipe_service: RecipeService=Depends(get_recipe_service)) -> int:
    return recipe_service.create_recipe(recipe)

@router.put("")
def update_recipe(recipe: RecipeDto, recipe_service: RecipeService = Depends(get_recipe_service)) -> int:
    return recipe_service.update_recipe(recipe)

@router.delete("/{recipe_id}")
def delete_recipe(recipe_id: int, recipe_service: RecipeService = Depends(get_recipe_service)) -> bool:
    recipe_service.delete_recipe(recipe_id)
    return True
