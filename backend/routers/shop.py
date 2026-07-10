
from fastapi import APIRouter, Cookie, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session
from database import get_session
from models.models import Team



router = APIRouter(prefix="/shop", tags=["shop"])

class SabotageRequest(BaseModel):
    team_id: str
    action: str    
    
class StealRequest(BaseModel):
    team_id: str

class ShopRequest(BaseModel):
    item: str

def get_team(team_id: str, session: Session):
    if not team_id:
        raise HTTPException(status_code=401, detail="Geen team")
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team niet gevonden")
    return team

@router.post("/sabotage", response_model=Team)
async def submit(body: SabotageRequest, team_id: str = Cookie(default=None), db: Session = Depends(get_session)):
    team = get_team(team_id, db)
    partner = get_team(body.team_id, db)
    
    if team.sabotage_coins < 1:
        raise HTTPException(status_code=400, detail="Niet genoeg shop coins")
    
    match body.action:
        case "blind":
            partner.blindfold += 1
        case "backwards":
            partner.backwards += 1
        case "half_likes":
            partner.multiplier *= 0.5
    
    team.sabotage_coins -= 1
    
    db.add(team)
    db.add(partner)
    db.commit()
    db.refresh(team)
    
    return team

@router.post("/steal", response_model=Team)
async def steal(body: StealRequest, team_id: str = Cookie(default=None), db: Session = Depends(get_session)):
    team = get_team(team_id, db)
    partner = get_team(body.team_id, db)
    
    if team.steal_coins < 1:
        raise HTTPException(status_code=400, detail="Niet genoeg steal coins")
    
    team.steal_coins -= 1
    
    if partner.block_steal:
        partner.block_steal = False
        db.add(team)
        db.add(partner)
        db.commit()    
        raise HTTPException(status_code=400, detail="Partner heeft stelen geblokkeerd")
    
    team.steal_task_id = partner.active_task_id
        
    db.add(team)
    db.add(partner)
    db.commit()
    db.refresh(team)
    
    return team

@router.post("/buy", response_model=Team)
async def buy(body: ShopRequest, team_id: str = Cookie(default=None), db: Session = Depends(get_session)):
    team = get_team(team_id, db)
    
    if team.shop_coins < 1:
        raise HTTPException(status_code=400, detail="Niet genoeg shop coins")
    
    match body.item:
        case "block_steal":
            team.block_steal = True
        case "extra":
            team.number_of_extras += 1
            
    team.shop_coins -= 1
    
    db.add(team)
    db.commit()
    db.refresh(team)
    
    return team
