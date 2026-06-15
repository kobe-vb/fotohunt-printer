from sqlmodel import SQLModel, Field, Relationship
from uuid import uuid4
from datetime import datetime

class Game(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    name: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Team(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    name: str
    game_id: str = Field(foreign_key="game.id")