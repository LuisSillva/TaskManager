from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_DIR = BASE_DIR / "data"
DATABASE_DIR.mkdir(exist_ok=True)  # creates the folder if it doesn't exist
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DATABASE_DIR}/tasks.db"

engine = create_engine(                                  # Conecta ao banco
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # Cria sessoes

Base = declarative_base() # base dos modelos

def get_db():              # fornece o banco pras rotas
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
