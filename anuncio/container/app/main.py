#
# main.py
#

from fastapi import FastAPI, APIRouter, Depends, HTTPException, status, UploadFile
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer

from modules.motando_authjwt import MotandoAuthJwt
from modules.motando_anuncio import MotandoAnuncio

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

    motando_authjwt = MotandoAuthJwt()    
    token_payload = motando_authjwt.verify_token(token)

    email = token_payload.get('email')

    return email


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
           motando_anuncio = MotandoAnuncio()
           motando_anuncio.email = email

           resp = motando_anuncio.add_img_tmp(filename=file.filename, data=img_data)   

           return JSONResponse(content=resp, status_code=resp.get('code'))

    resp = {'status': 'fail', 'message': 'Tipo/Tamanho da imagem não suportado.', 'code': 415}

    return JSONResponse(content=resp, status_code=resp.get('code'))


app.include_router(router)