from fastapi import FastAPI
from app.routers import tasks
from app.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(tasks.router)
