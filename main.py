from fastapi import FastAPI, Query, Path, status, HTTPException
from typing import Annotated
from models import *
from dotenv import load_dotenv
import httpx
import os

app = FastAPI()
load_dotenv()
API_KEY = os.getenv("AWESOME_API_KEY")
API_URL = f"https://economia.awesomeapi.com.br/json/last/USD-BRL,EUR-BRL"

@app.post("/registrar")
async def create_user(
        nome: Annotated[str, Query(max_length=100)], 
        email: Annotated[str, Query(max_length=100)], 
        senha: str
    ):
    """
    Cadastra um novo usuário no sistema.

    - **nome**: Nome do usuário (ex: Humberto).
    - **email**: Email do usuário (ex: mochilamonsterhigh@gmail.com).
    - **senha**: Senha de autenticação do usuário.
    """
    new_user = Usuario(
        nome=nome,
        email=email,
        senha=senha
    )
    return new_user

@app.post("/login")
async def user_login():
    pass

# API de Cotações de Moedas
@app.get("/consultar")
async def consult():
    if not API_KEY:
        raise HTTPException(status_code=500, detail="API key não configurada")
    
    async with httpx.AsyncClient() as client:
        resp = await client.get(API_URL, timeout=10.0)
    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code, detail=resp.json())
    return resp.json()
