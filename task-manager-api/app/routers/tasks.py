from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from typing import List, Optional

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)

@router.post('', response_model=TaskResponse, status_code=201) # cria objetos
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    new_task = Task(title=task.title, done=False)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@router.get('', response_model=List[TaskResponse]) # sem id especifico, retorna tudo
def get_tasks(
    done: Optional[bool] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
    ):
    query = db.query(Task)

    if done is not None:
        query = query.filter(Task.done == done)
    
    if search is not None:
        query = query.filter(Task.title.contains(search))
    
    return query.offset(skip).limit(limit).all()

@router.get('/{task_id}', response_model=TaskResponse) # lê informações, retorna ID especifico
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail='Task not found')
    return task

@router.put("/{task_id}", response_model=TaskResponse) # atualiza, update
def update_task(task_id: int, updated: TaskUpdate, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail='Task not found')
    if updated.title is not None:
        task.title = updated.title
    if updated.done is not None:
        task.done = updated.done
    db.commit()
    db.refresh(task)
    return task

@router.delete('/{task_id}', status_code=204)
def delete_task(task_id: int, db:Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail='Task not found')
    db.delete(task)
    db.commit()
