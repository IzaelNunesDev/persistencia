import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# Configuração do banco de dados para produção
DATABASE_URL = os.getenv("DATABASE_URL")

# Se não houver DATABASE_URL, usar configuração local
if not DATABASE_URL:
    DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/saneamento_ceara"

# Configurações do engine para produção
engine_kwargs = {
    "pool_pre_ping": True,
    "pool_recycle": 300,
    "pool_size": 10,
    "max_overflow": 20
}

engine = create_engine(DATABASE_URL, **engine_kwargs)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 