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


class UsuarioParticular():
    def __init__(self):
        global API_HOSTNAME

        self.__endpoint = f'http://{API_HOSTNAME}'    
    
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

    def get_profile(self, jwt_token: str = None) -> dict:
        """Obtém dados do perfil do usuário.

        Returns:
            Retorna um dicionário contendo os dados do perfil do usuário.        
        """
        url = f'{self.__endpoint}/usuario/particular'

        headers = {'Authorization': f'Bearer {jwt_token}'}

        try:
            resp = requests.get(url, headers=headers)
        except Exception as e:
            # TODO: Registrar em Log o insucesso.            
            return {'status ': 'error', 'message': 'Erro interno do servidor.', 'code': 500}
        else:
            resp.close()
    
        return resp.json()
    
    



