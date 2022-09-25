#
# frontend/container-app/app/modules/motando_anuncio.py
#

import os
import re
import json

import requests

#
# Globals
#
API_HOSTNAME = os.environ.get('MOTANDO_API_HOSTNAME')


class MotandoAnuncio():
    def __init__(self):
        global API_HOSTNAME

        self.__endpoint = f'http://{API_HOSTNAME}'    
    
    @property
    def jwt_token(self) -> str:
        return self._jwt_token
    
    @jwt_token.setter
    def jwt_token(self, jwt_token: str):
        self._jwt_token = jwt_token
    
    def add_img(self, filename: str = None, data: str = None) -> dict:
        """Adiciona uma imagem de anúncio através da sua API.
        
        """
        url = f'{self.__endpoint}/anuncio/imagem'

        headers = {'Authorization': f'Bearer {self._jwt_token}'}

        try:
            resp = requests.post(url, headers=headers, data={f'{filename}': data})
        except Exception as e:
            # TODO: Registrar em Log o insucesso.            
            return {'status ': 'error', 'message': 'Erro interno do servidor.', 'code': 500}
        else:
            resp.close()
        
        return resp.json()