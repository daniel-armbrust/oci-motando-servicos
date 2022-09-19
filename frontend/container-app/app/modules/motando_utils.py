#
# frontend/container-app/app/modules/motando_utils.py
#

import os
import base64
from functools import wraps

from flask import request, redirect, url_for
import oci
import requests

from .motando_authcookie import MotandoAuthCookie

#
# Globals
#
API_HOSTNAME = os.environ.get('MOTANDO_API_HOSTNAME')
CSRF_SECRETKEY_ID = os.environ.get('MOTANDO_CSRF_SECRETKEY_ID')
AUTH_COOKIE_NAME = os.environ.get('MOTANDO_AUTH_COOKIE_NAME')


def auth_service(email: str = None, senha: str = None):
    """Função que chama o serviço de autenticação dos usuários.

    """
    global API_HOSTNAME

    endpoint = f'http://{API_HOSTNAME}/login'

    payload = {
        'email': email,
        'senha': senha
    }

    try:
        resp = requests.post(endpoint, json=payload)
    except Exception as e:
        # TODO: Registrar em Log o insucesso.
        return None
    else:
        resp.close()
    
    return resp.json()


def get_csrf_secretkey() -> str:
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


def ensure_logged_in(fn):  
    @wraps(fn)
    def wrapper(*args, **kwargs):
        global AUTH_COOKIE_NAME

        cookie_value = request.cookies.get(AUTH_COOKIE_NAME, '')              

        if cookie_value:
            auth_cookie = MotandoAuthCookie()

            valid = auth_cookie.is_valid(cookie_value)            

            if not valid:
                return redirect(url_for('logout'))
                
        else:            
            return redirect(url_for('home'))

        return fn(*args, **kwargs)

    return wrapper
