# backend/app/routers/recipes.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas
from ..database import get_db
from .. import models
from .auth import get_current_user
from app import models



router = APIRouter(
    # We can define a prefix and tags for this router
    prefix="/recipes",
    tags=["Recipes"]
)

@router.get("/", response_model=List[schemas.Recipe])
def read_recipes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve a list of all recipes.
    """
    recipes = crud.get_recipes(db, skip=skip, limit=limit)
    return recipes


@router.post("/", response_model=schemas.Recipe, status_code=status.HTTP_201_CREATED)
def create_recipe(recipe: schemas.RecipeCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    """
    Create a new recipe.
    This endpoint is protected. The user is identified via their auth token.
    """
    # We pass the full user object to the crud function
    return crud.create_recipe(db=db, recipe=recipe, owner=current_user)

@router.get("/{recipe_id}", response_model=schemas.Recipe)
def read_recipe(recipe_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single recipe by its ID.
    """
    db_recipe = crud.get_recipe(db, recipe_id=recipe_id)
    if db_recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return db_recipe


@router.put("/{recipe_id}", response_model=schemas.Recipe)
def update_existing_recipe(recipe_id: int, recipe_update: schemas.RecipeCreate, db: Session = Depends(get_db)):
    """
    Update a recipe's title or description.
    """
    db_recipe = crud.update_recipe(db, recipe_id=recipe_id, recipe_update=recipe_update)
    if db_recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return db_recipe


@router.delete("/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_recipe(recipe_id: int, db: Session = Depends(get_db)):
    """
    Delete a recipe.
    """
    db_recipe = crud.delete_recipe(db, recipe_id=recipe_id)
    if db_recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    # A 204 response has no body, so we don't return anything
    return
