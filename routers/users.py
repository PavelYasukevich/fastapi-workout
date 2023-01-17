from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, Path

from models import Gender, Role, User, UserUpdate

router = APIRouter()

db: List[User] = [
    User(
        id=UUID("6cd85769-ff5c-4ba6-8508-45f00d445e9d"),
        first_name="Jamila",
        last_name="Ahmed",
        gender=Gender.female,
        roles=[Role.student],
    ),
    User(
        id=UUID("c46be086-b0b2-4abb-bab2-87d4716eda58"),
        first_name="Alex",
        last_name="Jones",
        gender=Gender.male,
        roles=[Role.admin, Role.user],
    ),
]


def get_user_or_404(user_id):
    for user in db:
        if user.id == user_id:
            return user
    raise HTTPException(
        status_code=404, detail=f"user with id: {user_id} does not exist"
    )


@router.get("/api/v1/users")
async def fetch_users():
    return db


@router.get("/api/v1/user")
async def get_user_by_name(name: Optional[str] = None):
    for user in db:
        if user.first_name == name or user.last_name == name:
            return user
    raise HTTPException(status_code=404, detail="User does not exist")


@router.post("/api/v1/users")
async def register_user(user: User):
    db.append(user)
    return {"id": user.id}


@router.delete("/api/v1/users/{user_id}")
async def delete_user(
    user_id: UUID = Path(None, description="The ID of user you want to delete")
):
    user = get_user_or_404(user_id)
    if user is not None:
        db.remove(user)


@router.put("/api/v1/users/{user_id}")
async def update_user(
    data: UserUpdate,
    user_id: UUID = Path(None, description="The ID of user you want to update"),
):
    user = get_user_or_404(user_id)
    if user is not None:
        if data.first_name is not None:
            user.first_name = data.first_name
        if data.last_name is not None:
            user.last_name = data.last_name
        if data.roles is not None:
            user.roles = data.roles
