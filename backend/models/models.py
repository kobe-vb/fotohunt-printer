import json
from datetime import datetime
from typing import Optional
from uuid import uuid4

from sqlmodel import UUID, Field, SQLModel


class Game(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    name: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Team(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    name: str
    game_id: str = Field(foreign_key="game.id", index=True)
    
    sabotage_coins: int = Field(default=0)
    shop_coins: int = Field(default=0)
    steal_coins: int = Field(default=0)
    
    number_of_extras: int = Field(default=0)
    block_steal: bool = Field(default=False)
    multiplier: float = Field(default=1.0)
    
    blindfold: int = Field(default=0)
    backwards: int = Field(default=0)

    active_task_id: Optional[str] = Field(default=None)
    steal_task_id: Optional[str] = Field(default=None)


class TaskRecord(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    team_id: str = Field(foreign_key="team.id", index=True)
    sequence_number: int

    assigned_at: datetime = Field(default_factory=datetime.utcnow)

    location_text: Optional[str] = Field(default=None)
    location_likes: Optional[int] = Field(default=None)
    pose_text: Optional[str] = Field(default=None)
    pose_likes: Optional[int] = Field(default=None)
    object_text: Optional[str] = Field(default=None)
    object_likes: Optional[int] = Field(default=None)
    
    copied_from: Optional[str] = Field(default=None)
    is_stolen: bool = Field(default=False)

    special_task_text: Optional[str] = Field(default=None)
    special_task_likes: Optional[int] = Field(default=None)

    extras_json: str = Field(default="[]")  # JSON: [{"text": "...", "likes": 3}, ...]

    photo_url: Optional[str] = Field(default=None)
    submitted_at: Optional[datetime] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    multiplier: float = Field(default=1.0)
    
    @property
    def is_stolen_copy(self) -> bool:
        return self.copied_from is not None

    @property
    def likes(self) -> int:
        if self.special_task_text is not None:
            return self.special_task_likes or 0
        return (self.location_likes or 0) + (self.pose_likes or 0) + (self.object_likes or 0)
    
    @property
    def bonus_likes(self) -> int:
        return sum(extra["likes"] for extra in self.extras)

    @property
    def extras(self) -> list[dict]:
        return json.loads(self.extras_json)

    def set_extras(self, extras: list[dict]):
        self.extras_json = json.dumps(extras)