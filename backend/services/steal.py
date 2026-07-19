


from sqlmodel import Session

from models.models import TaskRecord, Team
from sqlmodel import select, func

def get_next_sequence(team_id: str, db: Session) -> int:
    count = db.exec(
        select(func.count(TaskRecord.id))
        .where(TaskRecord.team_id == team_id)
    ).one()
    return count + 1
 


def steal_task(team_id: str, original_task_id: str, db: Session) -> TaskRecord:
    if not original_task_id:
        raise ValueError()
    team = db.get(Team, team_id)
    original = db.get(TaskRecord, original_task_id)

    if not team or not original:
        raise ValueError()

    if original.photo_url:
        raise ValueError("Task is al voltooid.")

    if team.steal_task_id:
        raise ValueError("Je hebt al een gestolen task.")

    seq = get_next_sequence(team_id, db)

    copied = TaskRecord(
        team_id=team_id,
        sequence_number=seq,
        location_text=original.location_text,
        location_likes=original.location_likes,
        pose_text=original.pose_text,
        pose_likes=original.pose_likes,
        object_text=original.object_text,
        object_likes=original.object_likes,
        extras_json=original.extras_json,
        copied_from=original.id,
        is_stolen_copy=True,
    )

    db.add(copied)
    db.flush()

    team.steal_task_id = copied.id

    db.add(team)
    db.commit()
    db.refresh(copied)

    return copied

def invalidate_original_task(stolen_task: TaskRecord, db: Session):
    if not stolen_task.copied_from:
        return

    original = db.get(TaskRecord, stolen_task.copied_from)

    if not original:
        return

    if original.photo_url:
        return

    original.is_stolen = True

    db.add(original)
    db.commit()