# backend/app/routers/users.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db
from .auth import pwd_context

router = APIRouter(
    prefix="/users",
    tags=["Users"] # This is for grouping in the API docs
)

@router.post("/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # 2. HASH THE PASSWORD HERE IN THE ENDPOINT
    hashed_password = pwd_context.hash(user.password)
    
    # 3. CALL THE UPDATED CRUD FUNCTION WITH THE HASHED PASSWORD
    return crud.create_user(db=db, user=user, hashed_password=hashed_password)
