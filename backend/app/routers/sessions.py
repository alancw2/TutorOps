from fastapi import APIRouter, HTTPException
from app import schemas
from app import storage

router = APIRouter(
    prefix="/sessions",
    tags=["sessions"]
)


@router.post("/", response_model=schemas.SessionOut)
def create_session(session: schemas.SessionCreate):
    client = storage.get_client_by_id(session.client_id)
    if client is None:
        raise HTTPException(status_code=404, detail="client not found")
    return storage.create_session(session.model_dump())


@router.get("/", response_model=list[schemas.SessionOut])
def list_sessions():
    return storage.list_sessions()


@router.get("/{session_id}", response_model=schemas.SessionOut)
def get_session_by_id(session_id: int):
    session = storage.get_session_by_id(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return session
