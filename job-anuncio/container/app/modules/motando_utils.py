#
# job-anuncio/container/app/modules/motando_utils.py
#

import os
import secrets
from datetime import datetime

import requests

#
# Globals
#
API_HOSTNAME = os.environ.get('MOTANDO_API_HOSTNAME')


def get_moto_marca(marca_id: int = None) -> dict:
    """Retorna as propriedades referente a Marca de uma motocicleta.

    """
    global API_HOSTNAME

    url = f'http://{API_HOSTNAME}/moto/marca/{marca_id}'

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


def get_moto_modelo(marca_id: int = None, modelo_id: int = None) -> dict:
    """Retorna as propriedades referente ao Modelo de uma motocicleta.

    """
    global API_HOSTNAME

    url = f'http://{API_HOSTNAME}/moto/marca/{marca_id}/modelo/{modelo_id}'

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


def return_randstr(token_len: int = 10):
    """Retorna uma string randômica.
    
    """
    randstr = secrets.token_hex(token_len) + datetime.now().strftime('%s%f')

    return randstr