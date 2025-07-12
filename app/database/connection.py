# app/database/connection.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# URI fornecida
DATABASE_URI = 'mysql+pymysql://sgls:ynFs42LpfsjGDEHP@132.226.249.149:3306/sgls'

# Criação do engine
engine = create_engine(DATABASE_URI, pool_pre_ping=True)

# Criação da sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Função utilitária para usar em rotas ou serviços
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

