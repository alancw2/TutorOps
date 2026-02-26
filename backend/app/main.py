from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import schemas
from app import storage
from app.routers.clients import router as clients_router
from app.routers.sessions import router as sessions_router


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(clients_router)
app.include_router(sessions_router)

@app.get("/health")
def health():
    return {"status":"ok"}

@app.get("/summary", response_model=schemas.GlobalSummaryOut)
def get_global_summary():
    return storage.get_global_summary()
