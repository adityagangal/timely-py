from fastapi import FastAPI
from app.routes import router as api_router
from database.config import connect_db, disconnect_db

app = FastAPI()

app.include_router(api_router)

@app.on_event("startup")
async def startup_event():
    await connect_db()

@app.on_event("shutdown")
async def shutdown_event():
    await disconnect_db()

