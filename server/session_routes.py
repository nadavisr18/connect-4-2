from typing import Dict

from fastapi import APIRouter
from fastapi.exceptions import HTTPException

from server import Session, SessionResponse
from .models import NewPlayer

session_router = APIRouter()

sessions: Dict[str, Session] = {}


def get_session(session_id: str) -> Session:
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    return sessions[session_id]


@session_router.post("/create_session")
async def create_session(new_player: NewPlayer) -> SessionResponse:
    session = Session()
    player = session.add_player(new_player.api)
    sessions[session.session_id] = session
    if len(sessions) > 100:
        sessions.pop(list(sessions.keys())[0])
    print(session)
    return SessionResponse(player=player, session_id=session.session_id)


@session_router.post("/join_session/{session_id}")
async def join_session(session_id: str, new_player: NewPlayer):
    session = get_session(session_id)
    player = session.add_player(new_player.api)
    return SessionResponse(player=player, session_id=session_id)
