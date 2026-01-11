from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from uuid import UUID


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class User(UserBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class CategoryBase(BaseModel):
    name: str


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = None


class Category(CategoryBase):
    id: UUID
    user_id: UUID

    class Config:
        from_attributes = True


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    is_completed: bool = False
    due_date: Optional[datetime] = None
    priority: int = 0


class TaskCreate(TaskBase):
    category_id: Optional[UUID] = None
    project_id: Optional[UUID] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None
    due_date: Optional[datetime] = None
    priority: Optional[int] = None
    category_id: Optional[UUID] = None
    project_id: Optional[UUID] = None


class Task(TaskBase):
    id: UUID
    user_id: UUID
    category_id: Optional[UUID] = None
    project_id: Optional[UUID] = None
    updated_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True


class ProjectBase(BaseModel):
    name: str


class ProjectCreate(ProjectBase):
    due_date: Optional[datetime] = None
    progress: int = 0


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    due_date: Optional[datetime] = None
    progress: Optional[int] = None


class Project(ProjectBase):
    id: UUID
    user_id: UUID
    create_day: datetime
    due_date: Optional[datetime] = None
    progress: int

    class Config:
        from_attributes = True