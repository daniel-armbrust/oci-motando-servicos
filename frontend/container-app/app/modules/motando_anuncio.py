#
# frontend/container-app/app/modules/motando_anuncio.py
#

import os
import re
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
        return self.__jwt_token
    
    @jwt_token.setter
    def jwt_token(self, jwt_token: str):
        self.__jwt_token = jwt_token

    def _format_data(self, data: dict = None) -> str:
        """Formata e ajusta os dados na padrão suportado pela API.
        
        """
        # Remove dados não usados vindos do formulário.
        data.pop('submit')
        data.pop('csrf_token')

        # Formata PRECO.
        br_preco = data.get('preco')
        str_preco = re.sub('[^\d\.]', '', br_preco.replace('.', '').replace(',', '.'))
        float_preco = float(str_preco)        
        
        data.update({'preco': format(float_preco, '.2f')})        

        # Remove caracteres de controles (\r\n) vindos da descrição do anúncio.
        descricao = motando_utils.remove_ctr_chars(data.get('descricao'))    
        data.update({'descricao': descricao})

        # Converte para uma lista de imagens.
        data.update({'img_lista': data.get('img_lista').split(',')})              

        json_str = json.dumps(data)

        return json_str

    def get(self, anuncio_id: int):
        """Obtém um anúncio específico.

        """
        url = f'{self.__endpoint}/anuncio/{anuncio_id}'

        headers = {'Authorization': f'Bearer {self.__jwt_token}'}

        try:
            resp = requests.get(url, headers=headers)
        except Exception as e:
            # TODO: Registrar em Log o insucesso.            
            return {'status ': 'error', 'message': 'Erro interno do servidor.', 'code': 500}
        else:
            resp.close()
        
        return resp.json()
    
    def list(self, offset: int = 0) -> dict:
        """Lista os anúncios.
        
        """
        url = f'{self.__endpoint}/anuncio'

        headers = {'Authorization': f'Bearer {self.__jwt_token}'}

        try:
            resp = requests.get(url, headers=headers)
        except Exception as e:
            # TODO: Registrar em Log o insucesso.            
            return {'status ': 'error', 'message': 'Erro interno do servidor.', 'code': 500}
        else:
            resp.close()
    
        return resp.json()        

    def add(self, data: dict = None) -> dict:
        """Adiciona um novo anúncio.
        
        """
        url = f'{self.__endpoint}/anuncio'

        headers = {
            'Authorization': f'Bearer {self.__jwt_token}',
            'Content-type': 'application/json'
        }

        json_data = self._format_data(data)              

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

        headers = {'Authorization': f'Bearer {self.__jwt_token}'}

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
    
    def update(self, anuncio_id: int, data: dict = None) -> dict:
        """Atualiza um anúncio.

        """
        url = f'{self.__endpoint}/anuncio/{anuncio_id}'

        headers = {
            'Authorization': f'Bearer {self.__jwt_token}',
            'Content-type': 'application/json'
        }

        json_data = self._format_data(data)              

        try:
            resp = requests.put(url, headers=headers, data=json_data)
        except Exception as e:
            # TODO: Registrar em Log o insucesso.            
            return {'status ': 'error', 'message': 'Erro interno do servidor.', 'code': 500}
        else:
            resp.close()
        
        return resp.json()  
