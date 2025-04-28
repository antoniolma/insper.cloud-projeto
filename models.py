from pydantic import BaseModel, Field
from typing import Annotated

class Usuario(BaseModel):
    nome: Annotated[str, Field(
        title="Nome do Usuário",
        description="Primeiro nome do usuário.",
        min_length=1,
        examples=["Humberto", "Pedro", "Antonio"]
    )]
    email : Annotated[str, Field(
        title="Email do Usuário",
        description="Email de login do usuário",
        examples=["mochilamonsterhigh@gmail.com", "humbertos@insper.edu.br", "pedronas@gmail.com"]
    )]
    senha : Annotated[str, Field(
        title="Senha do Usuário",
        description="Senha de acesso do usuário",
    )]