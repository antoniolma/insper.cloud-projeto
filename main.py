from fastapi import FastAPI, Query, Path, status, HTTPException
from typing import Annotated
from models import *

app = FastAPI()

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

@app.get("/consultar")
async def consult():
    pass