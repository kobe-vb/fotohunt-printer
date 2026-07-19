from fastapi import APIRouter, Depends, HTTPException, UploadFile, Cookie
from fastapi.params import File
from sqlmodel import Session
from database import get_session
from models.models import TaskRecord
from models.task import TaskResponse
from services.PrinterQueue import PrinterQueue, get_printer_Queue
from services.submission import generate_new_task, handle_submission

router = APIRouter(prefix="/task", tags=["teams"])

@router.post("/{task_id}/submit", response_model=TaskResponse)
async def submit(task_id: str, team_id: str = Cookie(default=None), photo: UploadFile = File(...), db: Session = Depends(get_session), printer: PrinterQueue = Depends(get_printer_Queue)):
    
    try:
        photo_bytes: bytes = await photo.read()
        new_task: TaskResponse = await handle_submission(task_id, team_id, photo_bytes, photo.filename, db, printer)
        return new_task
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/new", response_model=TaskResponse)
async def new(team_id: str = Cookie(default=None), db: Session = Depends(get_session), printer: PrinterQueue = Depends(get_printer_Queue)):
    
    try:
        new_task: TaskResponse = await generate_new_task(team_id, db, printer)
        return new_task
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: str, db: Session = Depends(get_session)):
    task = db.get(TaskRecord, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task niet gevonden ")
    return TaskResponse.from_record(task)

