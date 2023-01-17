from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Gender(str, Enum):
    male = 'male'
    female = 'female'


class Role(str, Enum):
    admin = 'admin'
    student = 'student'
    user = 'user'


class User(BaseModel):
    id: Optional[UUID] = Field(default_factory=uuid4)
    first_name: str
    last_name: str
    gender: Gender
    roles: List[Role]


class UserUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    roles: Optional[List[Role]]


class Post(BaseModel):
    id: Optional[int]
    # author: User
    title: str
    content: str
    created: datetime = Field(default_factory=datetime.utcnow)


class PostUpdate(BaseModel):
    title: Optional[str]
    content: Optional[str]
