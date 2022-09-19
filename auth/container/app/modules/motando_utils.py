#
# auth/container/app/modules/motando_utils.py
#

import os
import base64
import time
import datetime

import oci
from passlib.context import CryptContext
from jose import jwt, JWTError

from .motando_nosql import NoSQL

#
# Globals
#
NOSQL_CMP = os.environ.get('MOTANDO_NOSQL_CMP')
NOSQL_USERS_TABLE_NAME = os.environ.get('MOTANDO_NOSQL_USUARIO_TABLE_NAME')
CSRF_SECRETKEY_ID = os.environ.get('MOTANDO_CSRF_SECRETKEY_ID')


def check_passwd(email: str, plain_passwd: str) -> bool:
    """Verifica se a senha do usuário é correta pela comparação do HASH salvo
       no banco de dados.
    
    """
    global NOSQL_CMP, NOSQL_USERS_TABLE_NAME      
                
    query = f'SELECT senha FROM {NOSQL_USERS_TABLE_NAME} WHERE email = "{email}" LIMIT 1'

    nosql = NoSQL(NOSQL_CMP)
    nosql_result = nosql.exec_query(query)

    if len(nosql_result) > 0:
        db_hash = nosql_result[0]['senha']
        pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')        
            
        return pwd_context.verify(secret=plain_passwd, hash=db_hash)

    else:
        return False


def get_secretkey() -> str:
    """Obtém o SECRET_KEY armazendo no OCI Vault.
    
    """
    global CSRF_SECRETKEY_ID

    signer = oci.auth.signers.InstancePrincipalsSecurityTokenSigner()

    region = signer.region

    secrets_client = oci.secrets.SecretsClient(config={'region': region}, signer=signer)

    resp = secrets_client.get_secret_bundle(secret_id=CSRF_SECRETKEY_ID, stage='LATEST')

    if resp.status == 200:
        base64_content = resp.data.secret_bundle_content.content
        txt_decoded = base64.b64decode(base64_content).decode()

        return txt_decoded

    else:
        raise RuntimeError('Falha ao obter o SECRET_KEY.')


def create_access_token(email: str) -> str:
    """Cria token JWT.

    """
    payload = {
        'email': email,
        'expires': round(time.time() + 3600)
    }

    # TODO: encrypt payload?

    secret_key = get_secretkey()

    token = jwt.encode(payload, secret_key, algorithm='HS256')

    return token


def verify_access_token(token: str) -> dict:
    """Verifica token JWT.

    """
    secret_key = get_secretkey()

    try:
        jwt_data = jwt.decode(token, secret_key, algorithms=['HS256'])
    except JWTError:
        return {'status': 'fail', 'message': 'Token inválido.', 'code': 400}
    
    if ('email' in jwt_data) and ('expires' in jwt_data):
        expires = jwt_data.get('expires')

        if datetime.now() > datetime.utcfromtimestamp(expires):
            return {'status': 'fail', 'message': 'Token expirado.', 'code': 403}
        else:
            return {'status': 'success', 'message': 'Token validado com sucesso.', 
                'data': {'email': jwt_data.get('email')}, 'code': 200}
    
    else:
        return {'status': 'fail', 'message': 'Token inválido.', 'code': 400}