from fastapi import APIRouter
from app import schemas
from fastapi import HTTPException
from app import storage

router = APIRouter(
    prefix="/sessions",
    tags=["sessions"]
)

@router.post("/", response_model = schemas.SessionOut)
def create_session(session: schemas.SessionCreate):
    new_session = session.model_dump()
    new_session["id"] = storage.next_session_id
    storage.next_session_id += 1
    storage.sessions_db.append(new_session)
    return new_session

@router.get("/", response_model=list[schemas.SessionOut])
def list_sessions():
    return storage.sessions_db

@router.get("/{session_id}", response_model=schemas.SessionOut)
def get_session_by_id(session_id: int):
    for s in storage.sessions_db:
        if (s["id"] == session_id):
            return s
    raise HTTPException(status_code=404, detail="Session not found")

