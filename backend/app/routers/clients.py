from fastapi import APIRouter
from app import schemas
from app import storage
from fastapi import HTTPException

#Helpers
def get_client_by_id(client_id: int):
    for c in storage.clients_db:
        if (c["id"] == client_id):
            return c
    return None


router = APIRouter(
    prefix="/clients",
    tags=["clients"]
)

@router.post("/", response_model=schemas.ClientOut)
def create_client(client: schemas.ClientCreate):
    new_client = client.model_dump()
    new_client["id"] = storage.next_client_id
    storage.next_client_id += 1
    storage.clients_db.append(new_client)
    return new_client

@router.get("/", response_model=list[schemas.ClientOut])
def list_clients():
    return storage.clients_db

@router.get("/{client_id}", response_model=schemas.ClientOut)
def get_client_out(client_id: int):
    client = get_client_by_id(client_id)
    if client is None: 
        raise HTTPException(status_code = 404, detail="client not found")
    return client


@router.get("/{client_id}/sessions", response_model=list[schemas.SessionOut])
def list_client_sessions(client_id: int):
    client = get_client_by_id(client_id)
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    client_sessions = []
    for s in storage.sessions_db:
        if (s["client_id"] == client_id):
            client_sessions.append(s)
    return client_sessions

@router.get("/{client_id}/summary", response_model=schemas.ClientSummaryOut)
def get_client_summary(client_id: int):
    #calculate total_sessions
    client = get_client_by_id(client_id)
    if client is None:
        raise HTTPException(status_code=404, detail="client not found")

    total_sessions = 0
    total_hours = 0.0
    total_earnings = 0.0
    for s in storage.sessions_db:
        if (s["client_id"] == client_id):
            total_sessions += 1
            total_hours += s["duration_hours"]
            total_earnings += s["duration_hours"] * client["hourly_rate"]
    return {
        "client_id": client_id,
        "total_sessions": total_sessions,
        "total_hours": total_hours,
        "total_earnings": total_earnings,
    }







