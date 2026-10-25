from pydantic import BaseModel , ConfigDict , Field


class PlayerBase(BaseModel):
    username : str= Field(min_length=3, max_length=20)
    country : str

class PlayerCreate(PlayerBase):
    pass

class Player(PlayerBase):
    id : int
    model_config = ConfigDict(from_attributes=True)


#part II
class ScoreBase(BaseModel):
    game_name:str
    points : int=Field(ge=0) # ge is >= #greater than equal to


class ScoreCreate(ScoreBase):
    pass

class Score(ScoreBase):
    id : int
    player_id :int
    model_config=ConfigDict(from_attributes=True)
