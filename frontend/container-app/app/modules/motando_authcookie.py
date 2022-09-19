#
# frontend/container-app/app/modules/motando_authcookie.py
#

import os
import secrets
import ast
from datetime import datetime

from .motando_crypto import MontadoCrypto
from .motando_nosql import NoSQL

#
# Globals
#
NOSQL_TABLE_NAME = os.environ.get('MOTANDO_NOSQL_SESSION_TABLE_NAME')


class MotandoAuthCookie():
    def __init__(self):
        self._random_id_len = 32   

    @property
    def email(self):
        return self.__email
    
    @email.setter
    def email(self, email: str = None):
        self.__email = email
    
    @property
    def jwt_token(self):
        return self.__jwt_token
    
    @jwt_token.setter
    def jwt_token(self, jwt_token: str = None):
        self.__jwt_token = jwt_token

    def __get_random_id(self):
        random_id = secrets.token_hex(self._random_id_len)
        ts = datetime.now().strftime('%s')

        return random_id + ts
    
    def __get_cookie_values(self, crypt_cookie_value: str = None) -> dict:
        """Descriptografa e retorna o dicionário de valores contidos no cookie.
        
        """
        motando_crypto = MontadoCrypto()

        cookie_values = motando_crypto.decrypt(crypt_cookie_value)      

        if not cookie_values:            
            return None
        
        try:
            cookie_dict = ast.literal_eval(cookie_values)
        except ValueError:
            return None
        else:
            return cookie_dict        

    def create(self) -> str:
        """Cria COOKIE de Autenticação e insere dados na tabela de sessão.

        Returns:
            Retorna um token de sessão randômico e o e-mail do usuário 
        criptografados.
        """
        global NOSQL_TABLE_NAME

        session_token = self.__get_random_id()

        cookie_dict = {
            'session_token': session_token,
            'jwt_token': self.__jwt_token,
            'email': self.__email
        }
        
        cookie_str = str(cookie_dict)
        
        motando_crypto = MontadoCrypto()
        cookie_crypt_value = motando_crypto.encrypt(cookie_str)
        
        #sign_data = motando_crypto.sign(cookie_crypt_value)

        if cookie_crypt_value:
            session_data = {
                'session_token': session_token,
                'jwt_token': self.__jwt_token,
                'digital_sign': '',
                'email': self.__email
            }

            nosql = NoSQL()

            added = nosql.add(data=session_data, table=NOSQL_TABLE_NAME)

            if added:
                return cookie_crypt_value

        return None
    
    def remove(self, crypt_cookie_value: str = None):
        """Remove o registro do cookie de autenticação se existir.

        """
        global NOSQL_TABLE_NAME
        
        cookie_dict = self.__get_cookie_values(crypt_cookie_value)

        if not cookie_dict:
            return None
        
        query = f'''
            DELETE FROM {NOSQL_TABLE_NAME} 
               WHERE session_token = "{cookie_dict['session_token']}" AND email = "{cookie_dict['email']}"
        '''

        nosql = NoSQL()

        nosql.query(query=query)

        return None

    def is_valid(self, crypt_cookie_value: str = None) -> bool:
        """Verifica se o cookie de autenticação é válido.

        Returns:
            Retorna True caso o cookie seja válido ou False caso contrário.        
        """
        global NOSQL_TABLE_NAME

        cookie_dict = self.__get_cookie_values(crypt_cookie_value)

        if not cookie_dict:
            return False
        
        query = f'''
           SELECT session_token, email FROM {NOSQL_TABLE_NAME} 
              WHERE session_token = "{cookie_dict['session_token']}" AND email = "{cookie_dict['email']}" LIMIT 1        
        '''     

        # TODO: validar a assinatura digital do cookie.

        nosql = NoSQL()

        nosql_result = nosql.query(query=query)
        
        if len(nosql_result) > 0:
            db_session_token = nosql_result[0]['session_token']
            db_email = nosql_result[0]['email']

            # FIXME: double check ??
            if (db_session_token == cookie_dict['session_token']) and (db_email == cookie_dict['email']):
                return True
        
        return False
    
    def get_jwt(self, crypt_cookie_value: str = None) -> str:
        """Retorna JWT TOKEN usado 

        """
        cookie_dict = self.__get_cookie_values(crypt_cookie_value)

        if not cookie_dict:
            return None
        else:
            return cookie_dict['jwt_token']