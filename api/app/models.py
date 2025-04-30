from pydantic import BaseModel, Field, EmailStr
from typing import Annotated
from sqlalchemy import Column, Integer, String

class UserCreate(BaseModel):
    nome: Annotated[str, Field(
        title="Nome do Usuário",
        description="Primeiro nome do usuário.",
        min_length=1,
        examples=["Humberto", "Pedro", "Antonio"]
    )]
    email : Annotated[EmailStr, Field(
        title="Email do Usuário",
        description="Email de login do usuário",
        examples=["mochilamonsterhigh@gmail.com", "humbertos@insper.edu.br", "pedronas@gmail.com"]
    )]
    senha : Annotated[str, Field(
        title="Senha do Usuário",
        description="Senha de acesso do usuário",
        examples=['HumbasBambas', '1234321', 'juju-rocks@23']
    )]

class UserLogin(BaseModel):
    email: Annotated[EmailStr, Field(
        title="Email do Usuário",
        description="Email de login do usuário",
        examples=["mochilamonsterhigh@gmail.com", "humbertos@insper.edu.br", "pedronas@gmail.com"]
    )]
    senha : Annotated[str, Field(
        title="Senha do Usuário",
        description="Senha de acesso do usuário",
        examples=['HumbasBambas', '1234321', 'juju-rocks@23']
    )]