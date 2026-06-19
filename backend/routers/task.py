from fastapi import APIRouter, Depends, HTTPException, UploadFile, Cookie
from fastapi.params import File
from pydantic import BaseModel
from sqlmodel import Session
from database import get_session
from models import TaskRecord
from services.PrinterQueue import PrinterQueue, get_printer_Queue
from task import assign_new_task, get_next_sequence, submit_task
from task_generator import generate_task


router = APIRouter(prefix="/task", tags=["teams"])

"""
type Extra = { text: string; likes: number };

type TaskRecord = {
  id: string;
  sequence_number: number;
  location_text: string;
  location_likes: number;
  pose_text: string;
  pose_likes: number;
  object_text: string;
  object_likes: number;
  extras: Extra[];
};
"""

class Extra(BaseModel):
    text: str
    likes: int

class TaskSubmit(BaseModel):
    id: str
    sequence_number: int
    location_text: str
    location_likes: int
    pose_text: str
    pose_likes: int
    object_text: str
    object_likes: int
    extras: list[Extra]
    

@router.post("/{task_id}/submit", response_model=TaskSubmit)
async def submit(task_id: str, team_id: str = Cookie(default=None), photo: UploadFile = File(...), db: Session = Depends(get_session), printer: PrinterQueue = Depends(get_printer_Queue)):
    
    try:
        photo_bytes = await photo.read()

        submit_task(task_id, photo_bytes, photo.filename, db)
        # await printer.print_submission(name, task)
        task: TaskRecord = generate_task(team_id, get_next_sequence(team_id, db))
        assign_new_task(task.team_id, db, task)
        
        # await printer.print_task(db.get(TaskRecord, task_id).team.name, task)
        
        # coin_type = random.random.choice(["sabotage", "shop", "steal"])
        # await printer.print_coins(db.get(TaskRecord, task_id).team.name, coin_type)
        
        # db coin ++

        return task
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{task_id}", response_model=TaskSubmit)
def get_task(task_id: str, db: Session = Depends(get_session)):
    task = db.get(TaskRecord, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task niet gevonden ")
    return TaskSubmit(**task.dict(), extras=task.extras)