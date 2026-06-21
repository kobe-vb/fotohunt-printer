import random

from sqlmodel import Session, func, select

from models.models import TaskRecord

# --- Woordenlijsten (uitbreiden naar smaak) ---

LOCATIONS = [
    "aan een bushalte",
    "voor een bloemist",
    "op een brug",
    "in een park",
    "voor een kerk",
    "bij een fontein",
    "op een marktplein",
    "voor een supermarkt",
]

POSES = [
    "zittend op de grond",
    "springend",
    "met armen wijd",
    "ruggelings naar de camera",
    "hurken",
    "staand op één been",
    "liggend",
    "klappend",
]

OBJECTS = [
    "een flesje water",
    "een paraplu",
    "een hoed",
    "een bloem",
    "een krant",
    "een rugzak",
    "een fiets",
    "een ballon",
]

EXTRAS = [
    "met een vreemdeling erbij",
    "met een dier in beeld",
    "met een voertuig op de achtergrond",
    "terwijl iemand naar je kijkt",
    "met minimaal 3 mensen in beeld",
]


def generate_task(team_id: str, sequence_number: int) -> TaskRecord:

    record = TaskRecord(
        team_id=team_id,
        sequence_number=sequence_number,
        location_text=random.choice(LOCATIONS),
        location_likes=random.randint(1, 3),
        pose_text=random.choice(POSES),
        pose_likes=random.randint(1, 3),
        object_text=random.choice(OBJECTS),
        object_likes=random.randint(1, 3),
    )

    # Optioneel 0-2 extras
    num_extras = random.randint(0, 2)
    if num_extras > 0:
        chosen = random.sample(EXTRAS, k=min(num_extras, len(EXTRAS)))
        record.set_extras([{"text": e, "likes": random.randint(1, 2)} for e in chosen])

    return record


