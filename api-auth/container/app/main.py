#
# auth/container/app/main.py
#

import os

from fastapi import FastAPI, APIRouter
from fastapi.responses import JSONResponse

from modules.motando_models import LoginModel
from modules import motando_utils

#
# FastAPI initialization
#
router = APIRouter()
app = FastAPI(openapi_url=None)


@router.post('/login')
def login(data: LoginModel) -> dict:
    """Função para validar o login de um usuário. Caso o email e senha sejam
    válidos, um cookie que identifica o usuário logado é enviado.
    
    """
    email = data.email
    senha = data.senha   

    valid_passwd = motando_utils.check_passwd(email=email, plain_passwd=senha)

    if valid_passwd:
        token = motando_utils.create_access_token(email=email)        

        jwt_token = {
           'status': 'success', 
           'data': {'access_token': token, 'token_type': 'Bearer'},
           'code': 200
        }

        return JSONResponse(content=jwt_token)
        
    else:
        msg = {'status': 'fail', 'message': 'E-mail ou senha invalido(s).', 'code': 401}

        return JSONResponse(content=msg, status_code=msg.get('code'))       


app.include_router(router)