from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from models.models import User, Category, Task
from schemas.schemas import UserCreate, UserUpdate, CategoryCreate, CategoryUpdate, TaskCreate, TaskUpdate
from uuid import UUID


# User CRUD
async def get_user(db: AsyncSession, user_id: UUID) -> User | None:
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, user: UserCreate) -> User:
    db_user = User(email=user.email, password_hash=user.password)  # Note: hash password in real app
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def update_user(db: AsyncSession, user_id: UUID, user_update: UserUpdate) -> User | None:
    update_data = user_update.model_dump(exclude_unset=True)
    if "password" in update_data:
        update_data["password_hash"] = update_data.pop("password")  # Hash it
    await db.execute(update(User).where(User.id == user_id).values(**update_data))
    await db.commit()
    return await get_user(db, user_id)


async def delete_user(db: AsyncSession, user_id: UUID) -> bool:
    result = await db.execute(delete(User).where(User.id == user_id))
    await db.commit()
    return result.rowcount > 0


# Category CRUD
async def get_categories(db: AsyncSession, user_id: UUID) -> list[Category]:
    result = await db.execute(select(Category).where(Category.user_id == user_id))
    return result.scalars().all()


async def get_category(db: AsyncSession, category_id: UUID, user_id: UUID) -> Category | None:
    result = await db.execute(select(Category).where(Category.id == category_id, Category.user_id == user_id))
    return result.scalar_one_or_none()


async def create_category(db: AsyncSession, category: CategoryCreate, user_id: UUID) -> Category:
    db_category = Category(name=category.name, user_id=user_id)
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return db_category


async def update_category(db: AsyncSession, category_id: UUID, category_update: CategoryUpdate, user_id: UUID) -> Category | None:
    update_data = category_update.model_dump(exclude_unset=True)
    await db.execute(update(Category).where(Category.id == category_id, Category.user_id == user_id).values(**update_data))
    await db.commit()
    return await get_category(db, category_id, user_id)


async def delete_category(db: AsyncSession, category_id: UUID, user_id: UUID) -> bool:
    result = await db.execute(delete(Category).where(Category.id == category_id, Category.user_id == user_id))
    await db.commit()
    return result.rowcount > 0


# Task CRUD
async def get_tasks(db: AsyncSession, user_id: UUID) -> list[Task]:
    result = await db.execute(select(Task).where(Task.user_id == user_id))
    return result.scalars().all()


async def get_task(db: AsyncSession, task_id: UUID, user_id: UUID) -> Task | None:
    result = await db.execute(select(Task).where(Task.id == task_id, Task.user_id == user_id))
    return result.scalar_one_or_none()


async def create_task(db: AsyncSession, task: TaskCreate, user_id: UUID) -> Task:
    db_task = Task(**task.model_dump(), user_id=user_id)
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task


async def update_task(db: AsyncSession, task_id: UUID, task_update: TaskUpdate, user_id: UUID) -> Task | None:
    update_data = task_update.model_dump(exclude_unset=True)
    await db.execute(update(Task).where(Task.id == task_id, Task.user_id == user_id).values(**update_data))
    await db.commit()
    return await get_task(db, task_id, user_id)


async def delete_task(db: AsyncSession, task_id: UUID, user_id: UUID) -> bool:
    result = await db.execute(delete(Task).where(Task.id == task_id, Task.user_id == user_id))
    await db.commit()
    return result.rowcount > 0