import json
from datetime import datetime
from typing import Optional
from uuid import uuid4

from sqlmodel import Field, SQLModel


class Game(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    name: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Team(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    name: str
    game_id: str = Field(foreign_key="game.id")

    sabotage_coins: int = Field(default=0)
    shop_coins: int = Field(default=0)
    steal_coins: int = Field(default=0)

    active_task_id: Optional[str] = Field(default=None)


class TaskRecord(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    team_id: str = Field(foreign_key="team.id")
    sequence_number: int

    assigned_at: datetime = Field(default_factory=datetime.utcnow)

    location_text: str
    location_likes: int
    pose_text: str
    pose_likes: int
    object_text: str
    object_likes: int
    extras_json: str = Field(default="[]")  # JSON: [{"text": "...", "likes": 3}, ...]

    photo_url: Optional[str] = Field(default=None)
    submitted_at: Optional[datetime] = Field(default=None)

    @property
    def likes(self) -> int:
        return self.location_likes + self.pose_likes + self.object_likes
    
    @property
    def bonus_likes(self) -> int:
        return sum(extra["likes"] for extra in self.extras)

    @property
    def extras(self) -> list[dict]:
        return json.loads(self.extras_json)

    def set_extras(self, extras: list[dict]):
        self.extras_json = json.dumps(extras)