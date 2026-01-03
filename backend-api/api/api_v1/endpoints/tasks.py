from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.schemas import Task, TaskCreate, TaskUpdate
from crud.crud import get_tasks, get_task, create_task, update_task, delete_task
from db.session import get_db
from uuid import UUID

router = APIRouter()


@router.get("/", response_model=list[Task])
async def read_tasks(user_id: UUID = Query(...), db: AsyncSession = Depends(get_db)):
    return await get_tasks(db, user_id)


@router.post("/", response_model=Task)
async def create_new_task(task: TaskCreate, user_id: UUID = Query(...), db: AsyncSession = Depends(get_db)):
    return await create_task(db, task, user_id)


@router.get("/{task_id}", response_model=Task)
async def read_task(task_id: UUID, user_id: UUID = Query(...), db: AsyncSession = Depends(get_db)):
    db_task = await get_task(db, task_id, user_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@router.put("/{task_id}", response_model=Task)
async def update_existing_task(task_id: UUID, task_update: TaskUpdate, user_id: UUID = Query(...), db: AsyncSession = Depends(get_db)):
    db_task = await update_task(db, task_id, task_update, user_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@router.delete("/{task_id}")
async def delete_existing_task(task_id: UUID, user_id: UUID = Query(...), db: AsyncSession = Depends(get_db)):
    success = await delete_task(db, task_id, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted"}