#
# main.py
#

import os

from fastapi import FastAPI, APIRouter
from fastapi.responses import JSONResponse

from modules.motando_moto import Marca, Modelo, Versao

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


@router.get('/moto/marca')
async def all_marcas() -> dict:
    """Retorna todas as Marcas de Motos cadastradas.

    """   
    global REGION, OBJSTG_NAMESPACE, BUCKET_NAME

    marca = Marca(REGION, OBJSTG_NAMESPACE, BUCKET_NAME)    
    data = marca.return_all()

    return JSONResponse(content=data, status_code=data.get('code'))


@router.get('/moto/marca/{marca_id}')
async def marca(marca_id: int) -> dict:
    """Retorna uma Marca de Moto em particular através do seu identificador.

    Args:
        marca_id: Identificador numérico de uma Marca de moto.
        
    """
    global REGION, OBJSTG_NAMESPACE, BUCKET_NAME

    marca = Marca(REGION, OBJSTG_NAMESPACE, BUCKET_NAME)    
    data = marca.return_by_id(marca_id)

    return JSONResponse(content=data, status_code=data.get('code'))


@router.get('/moto/marca/{marca_id}/modelo')
async def all_modelos(marca_id: int) -> dict:
    """Retorna todos os Modelos de uma Marca de moto cadastrados.

    """   
    global REGION, OBJSTG_NAMESPACE, BUCKET_NAME

    modelo = Modelo(REGION, OBJSTG_NAMESPACE, BUCKET_NAME)    
    data = modelo.return_all(marca_id)

    return JSONResponse(content=data, status_code=data.get('code'))


@router.get('/moto/marca/{marca_id}/modelo/{modelo_id}')
async def modelo(marca_id: int, modelo_id: int) -> dict:
    """Retorna um Modelo de uma Marca de moto em particular através do seu
    identificador.

    Args:
        marca_id: Identificador numérico de uma Marca de moto.
        modelo_id: Identificador numérico de um Modelo pertencente a uma
    Marca de moto.

    """   
    global REGION, OBJSTG_NAMESPACE, BUCKET_NAME

    modelo = Modelo(REGION, OBJSTG_NAMESPACE, BUCKET_NAME)    
    data = modelo.return_by_id(marca_id, modelo_id)

    return JSONResponse(content=data, status_code=data.get('code'))


@router.get('/moto/marca/{marca_id}/modelo/{modelo_id}/versao')
async def all_versao(marca_id: int, modelo_id: int) -> dict:
    """Retorna todas as Versões pertencentes a um Modelo de uma Marca de moto 
    cadastrado.

    Args:
        marca_id: Identificador numérico de uma Marca de moto.
        modelo_id: Identificador numérico de um Modelo pertencente a uma
    Marca de moto.

    """   
    global REGION, OBJSTG_NAMESPACE, BUCKET_NAME

    versao = Versao(REGION, OBJSTG_NAMESPACE, BUCKET_NAME)    
    data = versao.return_all(marca_id, modelo_id)

    return JSONResponse(content=data, status_code=data.get('code'))


@router.get('/moto/marca/{marca_id}/modelo/{modelo_id}/versao/{versao_id}')
async def versao(marca_id: int, modelo_id: int, versao_id: int) -> dict:
    """Retorna todas as Versões pertencentes a um Modelo de uma Marca de moto 
    cadastrado.

    Args:
        marca_id: Identificador numérico de uma Marca de moto.
        modelo_id: Identificador numérico de um Modelo pertencente a uma
    Marca de moto.
        versao_id: Identificador numérico de uma Versão  

    """   
    global REGION, OBJSTG_NAMESPACE, BUCKET_NAME

    versao = Versao(REGION, OBJSTG_NAMESPACE, BUCKET_NAME)    
    data = versao.return_by_id(marca_id, modelo_id, versao_id)

    return JSONResponse(content=data, status_code=data.get('code'))


app.include_router(router)