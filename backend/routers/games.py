from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database import get_session
from models.models import Game
from pydantic import BaseModel

router = APIRouter(prefix="/games", tags=["games"])

class GameCreate(BaseModel):
    name: str

@router.get("", response_model=list[Game])
def get_games(session: Session = Depends(get_session)):
    return session.exec(select(Game)).all()

@router.post("", response_model=Game)
def create_game(body: GameCreate, session: Session = Depends(get_session)):
    game = Game(name=body.name)
    session.add(game)
    session.commit()
    session.refresh(game)
    return game