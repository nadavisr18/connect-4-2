from fastapi import APIRouter
from fastapi.exceptions import HTTPException

from game.data_models import Player
from .models import Move
from .session_routes import get_session

game_router = APIRouter()


@game_router.get("/board/{session_id}")
async def get_board(session_id: str):
    session = get_session(session_id)
    return session.board.get_json()


@game_router.post("/move/{session_id}")
async def insert(move: Move, session_id: str) -> bool:
    """
    returns whether this move won the game
    """
    session = get_session(session_id)
    try:
        session.board.insert(move.column, move.player)
        winner = session.board.check_win()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return winner[0]


@game_router.get("/check_win/{session_id}")
async def check_win(session_id: str):
    session = get_session(session_id)
    winner = session.board.check_win()
    return {"winner": winner[1].value if winner[0] else None}


@game_router.get("/current_turn/{session_id}")
async def current_turn(session_id: str) -> Player:
    session = get_session(session_id)
    return Player.O if session.board.last_move.player == Player.X else Player.X
