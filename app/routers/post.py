from typing import Optional
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import model, oauth2, schema
from ..database import get_db


router = APIRouter(prefix="/posts", tags=["Posts"])


def find_post(db: Session, post_id: str):
    return db.query(model.Post).filter(model.Post.id == post_id).first()


# GET Request
@router.get("/")
def get_post(
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth2.get_current_user),
    search: Optional[str] = "",
    limit: int = 10,
):
    print(limit)
    post = (
        db.query(model.Post)
        .filter(model.Post.user_id == current_user.id)
        .filter(model.Post.title.contains(search))
        .order_by(model.Post.created_at.desc())
        .limit(limit)
        .all()
    )
    return {"data": post}


# POST Requests
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.Post)
def create_posts(
    post: schema.PostCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth2.get_current_user),
):
    print(current_user)
    new_post_data = post.model_dump()
    new_post = model.Post(**new_post_data, user_id=current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# GET Request by ID
@router.get("/{id}")
def get_post(
    id: str,
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth2.get_current_user),
):
    print(current_user)
    post = find_post(db, id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} was not found",
        )
    return {"post_detail": post}


# Update by ID
@router.put("/{id}", response_model=schema.Post)
def update_post(
    id: str,
    updated_post: schema.PostCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth2.get_current_user),
):
    existing_post = find_post(db, id)
    if existing_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} was not found",
        )

    if existing_post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User not authorized to update post",
        )

    for key, value in updated_post.model_dump().items():
        setattr(existing_post, key, value)

    db.commit()
    return existing_post


# DELETE Request
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: str,
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth2.get_current_user),
):
    print(current_user)
    post = find_post(db, id)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} was not found",
        )
    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User not authorized to delete post",
        )
    db.delete(post)
    db.commit()
    return {"message": "Post deleted successfully"}
