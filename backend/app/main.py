from fastapi import FastAPI 
import app.routers.clients as clients


app = FastAPI()

app.include_router(clients.router)
@app.get("/health")
def health():
    return {"status":"ok"}
