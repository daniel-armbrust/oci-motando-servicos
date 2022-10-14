#
# frontend/container-app/app/modules/motando_usuario.py
#

import os
import re
import json

import requests

#
# Globals
#
API_HOSTNAME = os.environ.get('MOTANDO_API_HOSTNAME')


class MotandoUsuarioParticular():
    def __init__(self):
        global API_HOSTNAME

        self.__endpoint = f'http://{API_HOSTNAME}'    
    
    @property
    def jwt_token(self):
        return self.__jwt_token
    
    @jwt_token.setter
    def jwt_token(self, jwt_token: str = None):
        self.__jwt_token = jwt_token
    
    def add(self, data: dict = None) -> dict:
        """Adiciona um novo usuário particular a partir de dados do formulário.
        
        """
        url = f'{self.__endpoint}/usuario/particular'

        headers = {'Content-type': 'application/json'}

        # Remove dados não usados vindos do formulário de cadastro.
        data.pop('submit')
        data.pop('csrf_token')
        
        # Retira caracteres deixando somente os números do telefone.
        data['telefone'] = re.sub('[\(\)\- ]', '', data.get('telefone'))

        json_data = json.dumps(data)

        try:
            resp = requests.post(url, headers=headers, data=json_data)
        except Exception as e:
            # TODO: Registrar em Log o insucesso.            
            return {'status ': 'error', 'message': 'Erro interno do servidor.', 'code': 500}
        else:
            resp.close()
        
        return resp.json()

    def get_profile(self) -> dict:
        """Obtém dados do perfil do usuário.

        Returns:
            Retorna um dicionário contendo os dados do perfil do usuário.        
        """
        url = f'{self.__endpoint}/usuario/particular'

        headers = {'Authorization': f'Bearer {self.__jwt_token}'}

        try:
            resp = requests.get(url, headers=headers)
        except Exception as e:
            # TODO: Registrar em Log o insucesso.            
            return {'status ': 'error', 'message': 'Erro interno do servidor.', 'code': 500}
        else:
            resp.close()
    
        return resp.json()
    
    
class MotandoUsuarioParticularAnuncio():
    def __init__(self):
        global API_HOSTNAME

        self.__endpoint = f'http://{API_HOSTNAME}'    
    
    @property
    def jwt_token(self):
        return self.__jwt_token
    
    @jwt_token.setter
    def jwt_token(self, jwt_token: str = None):
        self.__jwt_token = jwt_token
    
    def get(self, anuncio_id: int):
        """Obtém um anúncio específico.

        """
        url = f'{self.__endpoint}/usuario/particular/anuncio/{anuncio_id}'

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
        """Lista os anúncios do usuário.
        
        """
        url = f'{self.__endpoint}/usuario/particular/anuncio'

        headers = {'Authorization': f'Bearer {self.__jwt_token}'}

        try:
            resp = requests.get(url, headers=headers)
        except Exception as e:
            # TODO: Registrar em Log o insucesso.            
            return {'status ': 'error', 'message': 'Erro interno do servidor.', 'code': 500}
        else:
            resp.close()
    
        return resp.json()        



