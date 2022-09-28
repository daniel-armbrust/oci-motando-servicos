#
# modules/motando_utils.py
#

import os
import requests

from passlib.context import CryptContext

#
# Globals
#
API_HOSTNAME = os.environ.get('MOTANDO_API_HOSTNAME')


def get_estado(estado_id=None):
    """Retorna as propriedades de um Estado em particular.

    Args:
        estado_id: Identificador numérico de um Estado.

    """
    global API_HOSTNAME

    url = f'http://{API_HOSTNAME}/brasil/estado/{estado_id}'

    resp = None

    try:
        resp = requests.get(url, timeout=10)
    except Exception as e:
        # TODO: Registrar em Log o insucesso.
        return None
    else:
        resp.close()

    if resp.status_code == 200:
        json = resp.json()

        return json['data']

    else:
        return None


def get_cidade(estado_id=None, cidade_id=None):
    """Retorna as propriedades de um Estado em particular.

    Args:
        estado_id: Identificador numérico de um Estado.
        cidade_id: Identificador numérico de uma Cidade.

    """
    global API_HOSTNAME

    url = f'http://{API_HOSTNAME}/brasil/estado/{estado_id}/cidade/{cidade_id}'

    resp = None

    try:
        resp = requests.get(url, timeout=10)
    except Exception as e:
        # TODO: Registrar em Log o insucesso.
        return None
    else:
        resp.close()

    if resp.status_code == 200:
        json = resp.json()

        return json['data']

    else:
        return None


def create_hash(password: str):
    """Retorna um HASH da string informada como parâmetro.
    
    """
    pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

    hash = pwd_context.hash(password)

    return hash