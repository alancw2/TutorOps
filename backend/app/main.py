from fastapi import FastAPI, HTTPException 
import app.routers.clients as clients
from app import schemas
from app import storage
from app.routers.clients import router as clients_router
from app.routers.sessions import router as sessions_router


#get Client by Id helper
def get_client_by_id(client_id: int):
    for c in storage.clients_db:
        if (c["id"] == client_id):
            return c
    return None


app = FastAPI()
app.include_router(clients_router)
app.include_router(sessions_router)

@app.get("/health")
def health():
    return {"status":"ok"}

@app.get("/summary", response_model=schemas.GlobalSummaryOut)
def get_global_summary():
    total_clients = 0
    total_sessions = 0
    total_hours = 0.0
    total_earnings = 0.0
    total_clients = len(storage.clients_db)
    for s in storage.sessions_db:
        client = get_client_by_id(s["client_id"])
        if client is None:
            HTTPException(status_code="404", detail="Client not found")
        total_sessions += 1
        total_hours += s["duration_hours"]
        total_earnings += s["duration_hours"] * client["hourly_rate"]
    return {
        "total_clients": total_clients,
        "total_sessions": total_sessions,
        "total_hours": total_hours,
        "total_earnings": total_earnings,
}
