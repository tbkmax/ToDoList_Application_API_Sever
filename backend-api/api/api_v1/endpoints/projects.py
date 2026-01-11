from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.schemas import Project, ProjectCreate, ProjectUpdate
from crud.crud import get_projects, get_project, create_project, update_project, delete_project
from db.session import get_db
from uuid import UUID

router = APIRouter()


@router.get("/", response_model=list[Project])
async def read_projects(user_id: UUID = Query(...), db: AsyncSession = Depends(get_db)):
    return await get_projects(db, user_id)


@router.post("/", response_model=Project)
async def create_new_project(project: ProjectCreate, user_id: UUID = Query(...), db: AsyncSession = Depends(get_db)):
    return await create_project(db, project, user_id)


@router.get("/{project_id}", response_model=Project)
async def read_project(project_id: UUID, user_id: UUID = Query(...), db: AsyncSession = Depends(get_db)):
    db_project = await get_project(db, project_id, user_id)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project


@router.put("/{project_id}", response_model=Project)
async def update_existing_project(project_id: UUID, project_update: ProjectUpdate, user_id: UUID = Query(...), db: AsyncSession = Depends(get_db)):
    db_project = await update_project(db, project_id, project_update, user_id)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project


@router.delete("/{project_id}")
async def delete_existing_project(project_id: UUID, user_id: UUID = Query(...), db: AsyncSession = Depends(get_db)):
    success = await delete_project(db, project_id, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"message": "Project deleted"}
