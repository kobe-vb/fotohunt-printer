import os
from datetime import datetime
from sqlmodel import Session, select, func
from models.models import TaskRecord, Team
from models.task import TaskResponse
from services.PrinterQueue import PrinterQueue
from services.task_generator import generate_task

PHOTO_DIR = "static/photos"

async def handle_submission(
    task_id: str,
    team_id: str,
    photo_bytes: bytes,
    filename: str,
    db: Session,
    printer: PrinterQueue,
) -> TaskResponse:
    
    old_task = db.get(TaskRecord, task_id)
    if not old_task:
        raise ValueError("Task niet gevonden")
    if old_task.photo_url:
        raise ValueError("Task al ingediend")

    team = db.get(Team, old_task.team_id)
    if not team:
        raise ValueError("Team niet gevonden")
    
    if team.id != team_id:
        raise ValueError("Dit is niet jouw task")

    submit_task(task_id, photo_bytes, filename, db)
    db.refresh(old_task)
    old_task_response = TaskResponse.from_record(old_task)
    
    seq = get_next_sequence(team.id, db)
    new_task = generate_task(team.id, seq)
    
    assign_new_task(team.id, db, new_task)

    db.refresh(new_task)    
    new_task_response = TaskResponse.from_record(new_task)

    await printer.print_submission(team.name, old_task_response)
    await printer.print_task(team.name, new_task_response)

    # 5. Coins (later) TODO
    # coin_type = random.choice(["sabotage", "shop", "steal"])
    # add_coin(team, coin_type, db)
    # await printer.print_coins(team.name, coin_type)

    return new_task_response

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