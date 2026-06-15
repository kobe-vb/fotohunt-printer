from fastapi import APIRouter, Depends, HTTPException, Response, Cookie
from sqlmodel import Session, select
from database import get_session
from models import Team, Game
from pydantic import BaseModel

router = APIRouter(prefix="/games/{game_id}/teams", tags=["teams"])

class TeamCreate(BaseModel):
    name: str

@router.get("/", response_model=list[Team])
def get_teams(game_id: str, session: Session = Depends(get_session)):
    if not session.get(Game, game_id):
        raise HTTPException(status_code=404, detail="Game niet gevonden")
    return session.exec(select(Team).where(Team.game_id == game_id)).all()

@router.post("/", response_model=Team)
def create_team(game_id: str, body: TeamCreate, response: Response, session: Session = Depends(get_session)):
    if not session.get(Game, game_id):
        raise HTTPException(status_code=404, detail="Game niet gevonden")
    
    team = Team(name=body.name, game_id=game_id)
    session.add(team)
    session.commit()
    session.refresh(team)

    response.set_cookie("team_id", team.id, httponly=True, samesite="lax")
    return team

@router.get("/me", response_model=Team)
def get_my_team(team_id: str = Cookie(default=None), session: Session = Depends(get_session)):
    if not team_id:
        raise HTTPException(status_code=401, detail="Geen team")
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team niet gevonden")
    return team