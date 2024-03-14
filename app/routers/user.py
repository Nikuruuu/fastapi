from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import model, schema, utils
from ..database import get_db

# Login
router = APIRouter(prefix="/users", tags=["Users"])


# POST User
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.UserOut)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user_data = user.model_dump()
    new_user = model.User(**new_user_data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# GET User
@router.get("/{id}", response_model=schema.UserOut)
def get_user(id: str, db: Session = Depends(get_db)):
    user = db.query(model.User).filter(model.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} does not found",
        )
    return user
