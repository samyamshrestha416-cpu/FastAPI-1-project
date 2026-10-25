from db import Base
from sqlalchemy import Integer, Column ,String ,ForeignKey

class Player(Base):
    __tablename__ = "players"

    id= Column(Integer ,primary_key=True,index=True)
    username = Column(String, unique=True, index=True)
    country = Column(String ,index=True)

    
#Part II
class Score(Base):
    __tablename__ ="scores"

    id = Column(Integer , primary_key=True ,index=True)
    player_id =Column(Integer ,ForeignKey("players.id"))
    game_name = Column(String ,index=True)
    points = Column(Integer)