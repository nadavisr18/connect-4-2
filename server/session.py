import uuid
from typing import List, Dict

from fastapi.exceptions import HTTPException
from pydantic import BaseModel, Field

from game import Board, Player


class SessionResponse(BaseModel):
    player: Player
    session_id: str


class Session(BaseModel):
    board: Board = Field(default_factory=lambda: Board())
    players: List[Player] = Field(default_factory=list)
    session_id: str = Field(default_factory=lambda: str(uuid.uuid4())[:5])
    player_apis: Dict[str, str] = Field(default_factory=dict)

    def add_player(self, api: str = None):
        if len(self.players) >= 2:
            raise HTTPException(status_code=400, detail="Session is full")
        player = Player.X if len(self.players) == 0 else Player.O
        self.players.append(player)
        if api:
            self.player_apis[player.value] = api
        return player

    @property
    def player_count(self):
        return len(self.players)

    class Config:
        arbitrary_types_allowed = True
