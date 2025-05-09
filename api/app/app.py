from fastapi import FastAPI, HTTPException, Depends, Query, Path, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from models import *
from dotenv import load_dotenv
import httpx
import os
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from passlib.context import CryptContext
import jwt as pyjwt
from jose import JWTError, jwt

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# SQLAlchemy setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# Obter hash da senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()

API_KEY = os.getenv("AWESOME_API_KEY")
API_URL = f"https://economia.awesomeapi.com.br/json/last/USD-BRL,EUR-BRL"
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

#########################################################################
# Classe Usuário

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

Base.metadata.create_all(bind=engine)

#########################################################################
# Auxiliares

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

security = HTTPBearer(auto_error=False)
async def verify_token(credentials: Annotated[HTTPAuthorizationCredentials, None] = Depends(security)):
    if credentials is None:
        return None
    
    token = credentials.credentials
    try:
        payload = pyjwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=403, detail="JWT ausente ou inválido.")

#########################################################################
# Endpoints

@app.post("/registrar", summary="Cria um novo usuário")
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Cadastra um novo usuário no sistema.

    - **nome**: Nome do usuário (ex: Humberto).
    - **email**: Email do usuário (ex: mochilamonsterhigh@gmail.com).
    - **senha**: Senha de autenticação do usuário.
    """
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=409, detail="Email já registrado.")
    new_user = User(
        nome=user.nome,
        email=user.email,
        hashed_password=get_password_hash(user.senha)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    to_encode = {"sub": new_user.email}
    encoded_jwt = pyjwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return {"jwt": encoded_jwt}  

@app.post("/login", summary="Login de usuário")
def user_login(user: UserLogin, db: Session = Depends(get_db)):
    """
    Login do Usuário já cadastrado.

    - **email**: Email do usuário (ex: mochilamonsterhigh@gmail.com).
    - **senha**: Senha de autenticação do usuário.
    """
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="Email não registrado.")
    
    # loginSenha = get_password_hash(user.senha)
    if not verify_password(user.senha, db_user.hashed_password):
        # print(f"User:  {db_user.hashed_password}")
        # print(f"login: {loginSenha}")
        raise HTTPException(status_code=401, detail="Senha não confere.")
        
    
    to_encode = {"sub": user.email}
    encoded_jwt = pyjwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return {"jwt": encoded_jwt}

# API de Cotações de Moedas
@app.get("/consultar", summary="Consulta cotações (requer token válido)")
async def consult(payload: dict = Depends(verify_token)):
    if payload is None:
        raise HTTPException(status_code=403, detail="JWT ausente ou inválido.")

    if not API_KEY:
        raise HTTPException(status_code=500, detail="API key não configurada.")
    
    async with httpx.AsyncClient() as client:
        resp = await client.get(API_URL, timeout=10.0)
    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code, detail=resp.json())
    return resp.json()