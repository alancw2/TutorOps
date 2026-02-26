from fastapi import APIRouter, HTTPException
from app import schemas
from app import storage


router = APIRouter(
    prefix="/clients",
    tags=["clients"]
)

@router.post("/", response_model=schemas.ClientOut)
def create_client(client: schemas.ClientCreate):
    return storage.create_client(client.model_dump())

@router.get("/", response_model=list[schemas.ClientOut])
def list_clients():
    return storage.list_clients()

@router.get("/{client_id}", response_model=schemas.ClientOut)
def get_client_out(client_id: int):
    client = storage.get_client_by_id(client_id)
    if client is None:
        raise HTTPException(status_code=404, detail="client not found")
    return client


@router.get("/{client_id}/sessions", response_model=list[schemas.SessionOut])
def list_client_sessions(client_id: int):
    client = storage.get_client_by_id(client_id)
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return storage.list_sessions_for_client(client_id)

@router.get("/{client_id}/summary", response_model=schemas.ClientSummaryOut)
def get_client_summary(client_id: int):
    summary = storage.get_client_summary(client_id)
    if summary is None:
        raise HTTPException(status_code=404, detail="client not found")
    return summary






