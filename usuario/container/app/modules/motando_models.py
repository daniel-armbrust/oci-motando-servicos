#
# modules/motando_models.py
#

import os
import re
from typing import List
from datetime import datetime

from pydantic import BaseModel, EmailStr, root_validator, validator, Field

from .motando_nosql import NoSQL

#
# Globals
#
NOSQL_TABLE_NAME = os.environ.get('MOTANDO_NOSQL_TABLE_NAME')


class UsuarioParticularModel(BaseModel):
    """Classe para novo cadastro de um Usuário Particular.
    
    """    
    brasil_estado: int
    brasil_cidade: int
    nome: str
    email: EmailStr
    email_confirm: EmailStr
    telefone: str = Field(..., exclude=True)
    senha: str = Field(..., exclude=True)
    senha_confirm: str

    @validator('email')
    def email_check_exists(cls, value):
        # TODO
        nosql = NoSQL()
        return value

    @validator('nome')
    def nome_validator(cls, value):
        if not re.match('^[A-Za-zÀ-ÿ\s]{1,150}$', value):
            raise ValueError('O nome inserido não é válido.')
        return value
    
    @validator('senha')
    def senha_validator(cls, value):
        if not re.match('^[A-Za-z0-9_!@#$%^&(*&) ]{10,}$', value):
            raise ValueError('A senha inserida não é válida.')
        return value

    @validator('telefone')
    def telefone_validator(cls, value):
        if not re.match('^[0-9]{8,}$', value):
            raise ValueError('O telefone inserido não é valido.')
        return value

    @root_validator
    def verify_match(cls, values):
        email = values.get('email')
        email_confirm = values.get('email_confirm')

        senha = values.get('senha')
        senha_confirm = values.get('senha_confirm')

        if email != email_confirm:         
            raise ValueError('Os e-mails inseridos não são iguais.')

        if senha != senha_confirm:
            raise ValueError('As senhas inseridas não são iguais.')        
        
        return values


class UsuarioParticularModelDb(BaseModel):
    __ts_now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

    email: EmailStr
    email_confirmado: bool = False
    nome: str
    senha: str = Field(..., min_length=50)
    admin: bool = False
    lojista: bool = False
    perfil_img_url: str = ''
    banner_img_url: str = ''
    telefone: List[dict] = []
    estado: str
    estado_sigla: str
    cidade: str
    cep: str = ''
    endereco: str = ''
    bairro: str = ''
    complemento: str = ''
    anuncio_id: List[int] = []
    data_cadastro: str = __ts_now
    data_modificacao: str = __ts_now


class UsuarioParticularModelOut(BaseModel):
    pass