
from fastapi import APIRouter, Depends, HTTPException, Response, Cookie
from sqlmodel import Session, select
from database import get_session
from models.task import TaskResponse
from services.PrinterQueue import get_printer_Queue
from models.models import TaskRecord, Team, Game
from pydantic import BaseModel

from services.PrinterQueue import PrinterQueue
from services.submission import assign_new_task
from services.task_generator import generate_task

router = APIRouter(prefix="/games/{game_id}/teams", tags=["teams"])

class TeamCreate(BaseModel):
    name: str

@router.get("", response_model=list[Team])
def get_teams(game_id: str, session: Session = Depends(get_session)):
    if not session.get(Game, game_id):
        raise HTTPException(status_code=404, detail="Game niet gevonden")
    return session.exec(select(Team).where(Team.game_id == game_id)).all()

@router.post("")
async def create_team(game_id: str, body: TeamCreate, response: Response, session: Session = Depends(get_session), printer: PrinterQueue = Depends(get_printer_Queue)):
    
    if not session.get(Game, game_id):
        raise HTTPException(status_code=404, detail="Game niet gevonden")
    
    if session.exec(select(Team).where(Team.game_id == game_id, Team.name == body.name)).first():
        raise HTTPException(status_code=400, detail="Teamnaam al in gebruik")
    
    team = Team(name=body.name, game_id=game_id)
    session.add(team)
    session.commit()
    session.refresh(team)

    response.set_cookie("team_id", team.id, httponly=True, samesite="lax")
    
    task: TaskRecord = generate_task(team.id, 1) # TODO: add simple task type
    assign_new_task(team.id, session, task)
    await printer.print_task(team.name, TaskResponse.from_record(task))
    
@router.get("/assign/{team_name}")
def assign_team(team_name: str, response: Response, session: Session = Depends(get_session)):
    team = session.exec(select(Team).where(Team.name == team_name)).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team niet gevonden")
    
    response.set_cookie("team_id", team.id, httponly=True, samesite="lax")
    return 

team_router = APIRouter(prefix="/teams", tags=["teams"])

@team_router.get("/me", response_model=Team)
def get_my_team(team_id: str = Cookie(default=None), session: Session = Depends(get_session)):
    if not team_id:
        raise HTTPException(status_code=401, detail="Geen team")
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team niet gevonden")
    return team