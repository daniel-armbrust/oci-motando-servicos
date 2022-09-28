#
# main.py
#

from fastapi import FastAPI, APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer

from modules.motando_models import UsuarioParticularModel
from modules.motando_usuario import UsuarioParticular
from modules.motando_authjwt import MotandoAuthJwt

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


@router.get('/usuario/particular')
async def usuario_particular(email: str = Depends(authenticate)):
    """Obtém dados do Usuário Particular.

    """
    usuario_particular = UsuarioParticular()
    resp = usuario_particular.get_profile(email)

    return JSONResponse(content=resp, status_code=resp.get('code'))


@router.post('/usuario/particular')
async def new_usuario_particular(data: UsuarioParticularModel) -> dict:
    """Cria um novo Usuário Particular.
    
    """
    usuario_particular = UsuarioParticular()
    resp = usuario_particular.add(data)

    return JSONResponse(content=resp, status_code=resp.get('code'))


app.include_router(router)