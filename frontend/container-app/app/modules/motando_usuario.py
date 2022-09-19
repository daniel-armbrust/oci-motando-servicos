#
# frontend/container-app/app/modules/motando_usuario.py
#

import os

import requests

#
# Globals
#
API_HOSTNAME = os.environ.get('MOTANDO_API_HOSTNAME')


class UsuarioParticular():
    def __init__(self):
        global API_HOSTNAME

        self.__endpoint = f'http://{API_HOSTNAME}'    
    
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
            print(str(e))
            return {'status ': 'fail', 'message': 'Usuário não encontrado', 'code': 404}
        else:
            resp.close()
    
        return resp.json()



