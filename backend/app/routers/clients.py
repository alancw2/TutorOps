from fastapi import APIRouter
from app.schemas import ClientCreate, ClientOut
from fastapi import HTTPException

router = APIRouter(
    prefix="/clients",
    tags=["clients"]
)

clients_db = []
next_id = 1

@router.post("/", response_model=ClientOut)
def create_client(client: ClientCreate):
    global next_id
    new_client = client.model_dump()
    new_client["id"] = next_id
    next_id += 1
    clients_db.append(new_client)
    return new_client

@router.get("/", response_model=list[ClientOut])
def list_clients():
    return clients_db

@router.get("/{client_id}", response_model=ClientOut)
def get_client_by_id(client_id: int):
    for c in clients_db:
        if (c["id"] == client_id):
            return c
    raise HTTPException(status_code=404, detail="Client not found")
    