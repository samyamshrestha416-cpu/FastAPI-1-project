from models import Player ,Score
from sqlalchemy.orm import Session
from schema import PlayerCreate ,ScoreCreate

def create_player(db : Session , data :PlayerCreate):
    player_instance = Player(**data.model_dump())
    db.add(player_instance)
    db.commit()
    db.refresh(player_instance)
    return player_instance

def get_players(db:Session):
    return db.query(Player).all()

def get_players_by_id(db:Session ,player_id:int):
    return db.query(Player).filter(Player.id == player_id).first()

def update_player(db: Session ,data:PlayerCreate,player_id : int):
    player_queryset = db.query(Player).filter(Player.id==player_id).first()
    if player_queryset:
        for key ,value in data.model_dump().items():
            setattr(player_queryset, key, value)    
        db.commit()
        db.refresh(player_queryset)
        return player_queryset


def delete_player(db: Session, player_id: int):
    player = db.query(Player).filter(Player.id == player_id).first()
    if player:
        db.delete(player)
        db.commit()
        return player

#if player has same usename it gives error and warning
def get_player_by_username(db: Session, username: str):
    return db.query(Player).filter(Player.username == username).first()


#Part II
def create_score(db: Session ,data: ScoreCreate ,player_id : int):
    score_instance=Score(**data.model_dump() ,player_id=player_id)
    db.add(score_instance)
    db.commit()
    db.refresh(score_instance)
    return score_instance

def get_score_by_player(db:Session ,player_id :int):
    return db.query(Score).filter(Score.player_id==player_id).all()

#Part III
def get_scores(db:Session ,game_name : str | None=None,limit:int=10 ):
    query = db.query(Score)
    if game_name:
        query = query.filter(Score.game_name==game_name)
    return query.limit(limit).all()

def get_leaderboard(db: Session ,game_name:str ):
    return(
        db.query(Score).filter(Score.game_name==game_name)
        .order_by(Score.points.desc())
        .limit(10)
        .all()
    )