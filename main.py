from fastapi import FastAPI , Depends ,HTTPException
import services,models,schema
from db import get_db , create_table
from sqlalchemy.orm import Session

create_table()

app = FastAPI()
@app.get("/players/", response_model=list[schema.Player])
def get_all_players(db :Session =Depends(get_db)):
    return services.get_players(db)

@app.get("/players/{id}",response_model=schema.Player)
def get_playerby_id(id:int ,db :Session =Depends(get_db)):
    PLayers_set= services.get_players_by_id(db, id)
    if PLayers_set:
        return PLayers_set
    raise HTTPException(status_code=404)

# @app.post("/players/",response_model=schema.Player)    #this is not used as username error does its thing frpm 39-44
# def Create_new_player(player: schema.PlayerCreate,db :Session =Depends(get_db)):
#   return services.create_player(db,player)

@app.put("/players/{id}",response_model=schema.Player)
def update_player(player:schema.PlayerCreate,id:int,db :Session =Depends(get_db)):
    db_update=services.update_player(db,player,id)
    if not db_update:
        raise HTTPException(status_code=404)
    return db_update

@app.delete("/players/{id}", response_model=schema.Player)
def delete_existing_player(id: int, db: Session = Depends(get_db)):
    db_delete=services.delete_player(db, id)
    if not db_delete:
        raise HTTPException(status_code=404)
    return db_delete

#username error code(if same username then error and warning)
@app.post("/players/", response_model=schema.Player)
def create_new_player(player: schema.PlayerCreate, db: Session = Depends(get_db)):
    existing = services.get_player_by_username(db, player.username)
    if existing:
        raise HTTPException(status_code=400, detail="Username already taken")
    return services.create_player(db, player)

#Part II
@app.post("/players/{id}/scores",response_model=schema.Score)
def add_score(id: int, score:schema.ScoreCreate ,db: Session = Depends(get_db)):
    player = services.get_players_by_id(db, id)
    if not player:
        raise HTTPException(status_code=404 ,detail="player not found")
    return services.create_score(db, score ,id)

@app.get("/players/{id}/scores",response_model=list[schema.Score])
def get_player_scores(id:int,db:Session = Depends(get_db)):
    player = services.get_players_by_id(db,id)
    if not player:
        raise HTTPException(status_code=404, detail="player not found")
    return services.get_score_by_player(db ,id)

#part III
@app.get("/scores/",response_model=list[schema.Score])
def list_scores(game_name:str | None=None ,limit:int=10,db:Session=Depends(get_db)):
    return services.get_scores(db, game_name,limit)

@app.get("/leaderboard/{game_name}", response_model=list[schema.Score])
def leaderboard(game_name: str,db:Session=Depends(get_db)):
    return services.get_leaderboard(db, game_name)