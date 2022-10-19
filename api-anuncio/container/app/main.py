#
# main.py
#

from fastapi import FastAPI, APIRouter, Depends, HTTPException, status, UploadFile
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer

from modules.motando_authjwt import AuthJwt
from modules.motando_models import AnuncioModel
from modules.motando_anuncio import Anuncio

#
# FastAPI initialization
#
router = APIRouter()
app = FastAPI(openapi_url=None)
oauth2_schema = OAuth2PasswordBearer(tokenUrl='/login')


async def authenticate(token: str = Depends(oauth2_schema)) -> str:
    """Função injetável para verificar se o usuário possui um Token JWT válido.

    Returns:
        Retorna o e-mail do usuário contido dentro do Token JWT.    
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Acesso negado.'
        )

    authjwt = AuthJwt()    
    token_payload = authjwt.verify_token(token)

    email = token_payload.get('email')

    return email


@router.get('/anuncio')
async def list_anuncio(offset: int = 0, email: str = Depends(authenticate)) -> dict:
    """Lista todos os anúncios.
    
    """
    anuncio = Anuncio()
    anuncio.email = email

    # TODO: paginador

    resp = anuncio.list(offset=offset)

    return JSONResponse(content=resp, status_code=resp.get('code')) 


@router.get('/anuncio/{anuncio_id}')
async def edit_anuncio(anuncio_id: int, email: str = Depends(authenticate)) -> dict:
    """Obtém todos os anúncios do usuário particular.
    
    """
    anuncio = Anuncio()
    anuncio.email = email

    resp = anuncio.get(anuncio_id=anuncio_id)

    return JSONResponse(content=resp, status_code=resp.get('code')) 


@router.put('/anuncio/{anuncio_id}')
async def update_anuncio(anuncio_id: int, data: AnuncioModel, email: str = Depends(authenticate)) -> dict:
    """Adiciona um novo Anúncio.

    """
    anuncio = Anuncio()
    anuncio.email = email

    resp = anuncio.update(anuncio_id=anuncio_id, data=data)
    
    return JSONResponse(content=resp, status_code=resp.get('code')) 


@router.post('/anuncio')
async def new_anuncio(data: AnuncioModel, email: str = Depends(authenticate)) -> dict:
    """Adiciona um novo Anúncio.

    """
    anuncio = Anuncio()
    anuncio.email = email

    resp = anuncio.add(data)
    
    return JSONResponse(content=resp, status_code=resp.get('code'))    


@router.post('/anuncio/imagem')
async def anuncio_imagem(file: UploadFile, email: str = Depends(authenticate)) -> dict:
    """Salva uma nova imagem.
    
    """
    allowed_mimetype = ('image/jpeg', 'image/png', 'image/webp',)
    max_img_size = 5242880

    if file.content_type in allowed_mimetype:
        img_data = await file.read()
        img_data_bytes = len(img_data)        

        if img_data_bytes > 0 and img_data_bytes <= max_img_size:
           anuncio = Anuncio()
           anuncio.email = email

           resp = anuncio.add_img_tmp(filename=file.filename, data=img_data)   

           return JSONResponse(content=resp, status_code=resp.get('code'))

    resp = {'status': 'fail', 'message': 'Tipo/Tamanho da imagem não suportado.', 'code': 415}

    return JSONResponse(content=resp, status_code=resp.get('code'))


app.include_router(router)