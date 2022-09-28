#
# main.py
#

import os

from fastapi import FastAPI, APIRouter
from fastapi.responses import JSONResponse

from modules.motando_estado_cidade import Estado, Cidade

#
# Globals
#
REGION = os.environ.get('MOTANDO_REGION')
OBJSTG_NAMESPACE = os.environ.get('MOTANDO_OBJSTG_NAMESPACE')
BUCKET_NAME = os.environ.get('MOTANDO_BUCKET_NAME')

#
# FastAPI initialization
#
router = APIRouter()
app = FastAPI(openapi_url=None)


@router.get('/brasil/estado')
async def all_estados() -> dict:
    """Retorna todos os Estados cadastrados.

    """
    global REGION, OBJSTG_NAMESPACE, BUCKET_NAME

    estado = Estado(REGION, OBJSTG_NAMESPACE, BUCKET_NAME)    
    data = estado.return_all()

    return JSONResponse(content=data, status_code=data.get('code'))


@router.get('/brasil/estado/{estado_id}')
async def estado(estado_id: int) -> dict:    
    """Retorna um Estado em particular através do seu identificador.

    Args:
        estado_id: Identificador numérico de um Estado.

    """
    global REGION, OBJSTG_NAMESPACE, BUCKET_NAME

    estado = Estado(REGION, OBJSTG_NAMESPACE, BUCKET_NAME)   
    data = estado.return_by_id(estado_id)
    
    return JSONResponse(content=data, status_code=data.get('code'))


async def add_estado():
    pass

async def update_estado():
    pass

async def remove_estado():
    pass


@router.get('/brasil/estado/{estado_id}/cidade')
async def all_cidades(estado_id: int) -> dict:
    """Retorna todas as Cidades de um Estado em particular através do seu
    identificador numérico.

    Args:
        estado_id: Identificador numérico de um Estado.
     
    """
    global REGION, OBJSTG_NAMESPACE, BUCKET_NAME

    cidade = Cidade(REGION, OBJSTG_NAMESPACE, BUCKET_NAME)    
    data = cidade.return_all(estado_id)    

    return JSONResponse(content=data, status_code=data.get('code'))


@router.get('/brasil/estado/{estado_id}/cidade/{cidade_id}')
async def cidade(estado_id: int, cidade_id: int) -> dict:
    """Retorna uma Cidade pertencente a um Estado.

    Args:
        estado_id: Identificador numérico de um Estado.
        cidade_id: Identificador numérico de uma Cidade.
     
    """
    global REGION, OBJSTG_NAMESPACE, BUCKET_NAME

    cidade = Cidade(REGION, OBJSTG_NAMESPACE, BUCKET_NAME)    
    data = cidade.return_by_id(estado_id, cidade_id)    
    
    return JSONResponse(content=data, status_code=data.get('code'))


app.include_router(router)