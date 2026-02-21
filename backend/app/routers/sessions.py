from fastapi import APIRouter
from app.schemas import SessionCreate, SessionOut
from fastapi import HTTPException

router = APIRouter(
    prefix="/sessions",
    tags=["sessions"]
)

sessions_db = []
next_session_id = 1

@router.post("/", response_model = SessionOut)
def create_session(session: SessionCreate):
    global next_session_id
    new_session = session.model_dump()
    new_session["id"] = next_session_id
    next_session_id += 1
    sessions_db.append(new_session)
    return new_session

@router.get("/", response_model=list[SessionOut])
def list_sessions():
    return sessions_db

@router.get("/{session_id}", response_model=SessionOut)
def get_session_by_id(session_id: int):
    for s in sessions_db:
        if (s["id"] == session_id):
            return s
    raise HTTPException(status_code=404, detail="Session not found")

