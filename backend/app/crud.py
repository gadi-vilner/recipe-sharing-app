# backend/app/crud.py

from sqlalchemy.orm import Session
from passlib.context import CryptContext
from . import models, schemas

# Create a CryptContext instance for password hashing
# We specify that 'bcrypt' is the hashing algorithm to use.
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_email(db: Session, email: str):
    """
    Query the database for a user with a specific email.
    """
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate, hashed_password: str):
    """
    Create a new user in the database.
    This function now expects the password to be already hashed.
    """
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password # We use the pre-hashed password directly
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_recipes(db: Session, skip: int = 0, limit: int = 100):
    """
    Retrieve a list of recipes with pagination.
    """
    return db.query(models.Recipe).offset(skip).limit(limit).all()

def create_recipe(db: Session, recipe: schemas.RecipeCreate, owner: models.User):
    """
    Create a new recipe associated with a user object.
    """
    # Create the Recipe instance, and let SQLAlchemy handle the relationship
    db_recipe = models.Recipe(**recipe.model_dump(), author=owner)
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe

def get_recipe(db: Session, recipe_id: int):
    """
    Retrieve a single recipe by its ID.
    """
    return db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()

def update_recipe(db: Session, recipe_id: int, recipe_update: schemas.RecipeCreate):
    """
    Update an existing recipe.
    """
    db_recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    if db_recipe:
        # Update model from the Pydantic schema
        update_data = recipe_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_recipe, key, value)
        db.commit()
        db.refresh(db_recipe)
    return db_recipe

def delete_recipe(db: Session, recipe_id: int):
    """
    Delete a recipe.
    """
    db_recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    if db_recipe:
        db.delete(db_recipe)
        db.commit()
    return db_recipe