#
# frontend/container-app/app/modules/motando_anuncio.py
#

import os
import ast
import json

import requests

from . import motando_utils

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
    
    def add(self, data: dict = None) -> dict:
        """Adiciona um novo anúncio.
        
        """
        url = f'{self.__endpoint}/anuncio'

        headers = {
            'Authorization': f'Bearer {self._jwt_token}',
            'Content-type': 'application/json'
        }

        # Remove dados não usados vindos do formulário de cadastro.
        data.pop('submit')
        data.pop('csrf_token')

        # Formata PRECO
        print(data.get('preco'))
        data.update({'preco': format(data.get('preco'), '.2f')})              

        try:
            img_lista = ast.literal_eval(data.get('img_lista'))
        except SyntaxError:
            return {'status ': 'fail', 'message': 'Sintaxe inválida ao processar os dados.', 'code': 400}
        else:            
            data.update({'img_lista': img_lista})  

        json_data = json.dumps(data)

        try:
            resp = requests.post(url, headers=headers, data=json_data)
        except Exception as e:
            # TODO: Registrar em Log o insucesso.            
            return {'status ': 'error', 'message': 'Erro interno do servidor.', 'code': 500}
        else:
            resp.close()
        
        return resp.json()
    
    def add_img(self, filename: str = None, data: str = None) -> dict:
        """Adiciona uma imagem de anúncio através da sua API.
        
        """
        url = f'{self.__endpoint}/anuncio/imagem'

        headers = {'Authorization': f'Bearer {self._jwt_token}'}

        mimetype = motando_utils.get_img_mimetype(data)

        file_data = (filename, data, mimetype)

        try:
            resp = requests.post(url, headers=headers, files={'file': file_data})
        except Exception as e:
            # TODO: Registrar em Log o insucesso.            
            return {'status ': 'error', 'message': 'Erro interno do servidor.', 'code': 500}
        else:
            resp.close()

        return resp.json()