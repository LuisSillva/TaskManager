from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import tasks
from app.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],         # lista de frontends permitidos a "conversar" com a API
    allow_credentials=True,
    allow_methods=["*"], # Todos os métodos http
    allow_headers=["*"],

)    


app.include_router(tasks.router)
