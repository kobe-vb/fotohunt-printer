


from datetime import datetime
import os
from sqlmodel import Session, select, func
from models import TaskRecord, Team

PHOTO_DIR = "static/photos"


def submit_task(task_id: str, photo_bytes: bytes, filename: str, db: Session):
    
    task = db.get(TaskRecord, task_id)
    if not task:
        raise ValueError("Task niet gevonden")

    if task.photo_url:
        raise ValueError("Task al ingediend")

    team = db.get(Team, task.team_id)
    if not team:
        raise ValueError("Team niet gevonden")

    os.makedirs(PHOTO_DIR, exist_ok=True)
    path = os.path.join(PHOTO_DIR, f"{task_id}_{filename}")

    with open(path, "wb") as f:
        f.write(photo_bytes)

    task.photo_url = f"/static/photos/{os.path.basename(path)}"
    task.submitted_at = datetime.utcnow()

    team.active_task_id = None

    db.add(task)
    db.add(team)

    db.commit()

    return 

def get_next_sequence(team_id: str, db: Session) -> int:
    count = db.exec(
        select(func.count(TaskRecord.id))
        .where(TaskRecord.team_id == team_id)
    ).one()
    return count + 1
    

def assign_new_task(team_id: str, db: Session, task: TaskRecord):
    team = db.get(Team, team_id)
    if not team:
        raise ValueError("Team niet gevonden")

    db.add(task)
    db.flush()  # task.id bestaat nu

    team.active_task_id = task.id
    db.add(team)

    db.commit()
    db.refresh(task)

    return 