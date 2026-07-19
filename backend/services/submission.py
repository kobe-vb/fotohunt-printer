import os
from datetime import datetime, timedelta
import random
from sqlmodel import Session, select, func
from models.models import TaskRecord, Team
from models.task import TaskResponse
from services.PrinterQueue import PrinterQueue
from services.steal import invalidate_original_task
from services.task_generator import task_generator

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
    # TODO: Uncomment this check if you want to enforce a minimum time between submissions
    if datetime.utcnow() - old_task.created_at < timedelta(minutes=3):
        raise ValueError(f"Task te snel ingediend, wacht {3 - (datetime.utcnow() - old_task.created_at).seconds // 60} minuten")

    team = db.get(Team, team_id)
    if not team:
        raise ValueError("Team niet gevonden")
    if team.active_task_id != task_id and team.steal_task_id != task_id:
        raise ValueError("Dit is niet jouw task")
    
    submit_task(task_id, team_id, photo_bytes, filename, db)
    db.refresh(old_task)
    # old_task_response = TaskResponse.from_record(old_task)
    
    seq = get_next_sequence(team.id, db)
    new_task = task_generator.genereer_taak(team.id, seq, extra_count=team.number_of_extras)
    
    assign_new_task(team.id, db, new_task, team.multiplier)

    db.refresh(new_task)    
    new_task_response = TaskResponse.from_record(new_task)

    # await printer.print_submission(team.name, old_task_response)
    await printer.print_task(team.name, new_task_response)

    coin_type = random.choices(["shop", "sabotage", "steal"], weights=[4, 2, 1], k=1)[0]
    add_coin(team, coin_type, db)
    await printer.print_coins(team.name, coin_type)
    
    team.backwards = max(0, team.backwards - 1)
    team.blindfold = max(0, team.blindfold - 1)
    
    team.multiplier = 1
    
    db.commit()
    db.refresh(team)

    return new_task_response

async def generate_new_task(
    team_id: str,
    db: Session,
    printer: PrinterQueue
) -> TaskResponse:

    team = db.get(Team, team_id)
    if not team:
        raise ValueError("Team niet gevonden")

    seq = get_next_sequence(team.id, db)
    new_task = task_generator.genereer_taak(team.id, seq, extra_count=team.number_of_extras)
    
    assign_new_task(team.id, db, new_task, team.multiplier)

    db.refresh(new_task)    
    new_task_response = TaskResponse.from_record(new_task)

    # await printer.print_submission(team.name, old_task_response)
    await printer.print_task(team.name, new_task_response)
    team.multiplier = 1
    
    db.commit()
    db.refresh(team)

    return new_task_response


def add_coin(team: Team, coin_type: str, db: Session):
    if coin_type == "shop":
        team.shop_coins += 1
    elif coin_type == "sabotage":
        team.sabotage_coins += 1
    elif coin_type == "steal":
        team.steal_coins += 1
    else:
        raise ValueError("Ongeldig type munt")
    
    db.add(team)
    db.commit()

def submit_task(task_id: str, team_id: str, photo_bytes: bytes, filename: str, db: Session):
    
    task = db.get(TaskRecord, task_id)
    if not task:
        raise ValueError("Task niet gevonden")

    if task.photo_url:
        raise ValueError("Task al ingediend")

    team = db.get(Team, team_id)
    if not team:
        raise ValueError("Team niet gevonden")
    
    if task.is_stolen_copy:
        invalidate_original_task(task, db)
        team.steal_task_id = None
        
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
    

def assign_new_task(team_id: str, db: Session, task: TaskRecord, multiplier: float=1.0):
    team = db.get(Team, team_id)
    if not team:
        raise ValueError("Team niet gevonden")

    task.multiplier = multiplier
    db.add(task)
    db.flush()  # task.id bestaat nu

    team.active_task_id = task.id
    db.add(team)

    db.commit()
    db.refresh(task)

    return