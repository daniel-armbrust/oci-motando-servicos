#
# modules/motando_usuario.py
#

import os
import datetime

from .motando_models import UsuarioParticularModel, UsuarioParticularModelDb
from .motando_nosql import NoSQL
from . import motando_utils

#
# Globals
#
NOSQL_TABLE_NAME = os.environ.get('MOTANDO_NOSQL_TABLE_NAME')


class UsuarioParticular():
    def __email_exists(self, email: str = None) -> bool:
        """Verifica se o e-mail informado já foi cadastrado.        
        
        """
        global NOSQL_TABLE_NAME

        query = f'SELECT email FROM {NOSQL_TABLE_NAME} WHERE email = "{email}" LIMIT 1'

        nosql = NoSQL()
        result = nosql.query(query)

        if len(result) > 0:
            return True
        else:
            return False

    def add(self, data: UsuarioParticularModel) -> dict:
        """Adiciona um novo usuário particular. 
        
        """
        global NOSQL_TABLE_NAME

        if self.__email_exists(data.email):
            return {'status': 'fail', 'message': 'O e-mail para cadastro já existe.', 'code': 409}

        estado_id = data.brasil_estado
        cidade_id = data.brasil_cidade
         
        # Obtém as propriedades do Estado a partir do ID recebido do formulário. 
        estado_data = motando_utils.get_estado(estado_id)       
    
        # Obtém as propriedades da Cidade a partir do ID recebido do formulário. 
        cidade_data = motando_utils.get_cidade(estado_id, cidade_id)

        if not estado_data or not cidade_data:
            return {'status': 'error', 'message': 'Erro interno do servidor.', 'code': 500}
        
        estado = estado_data[0]['estado']
        estado_sigla = estado_data[0]['sigla']
        cidade = cidade_data[0]['cidade']

        # Substituí o campo telefone por uma LISTA que contém telefones e suas propriedades.    
        telefone = [{'telefone': data.telefone, 'whatsapp': False, 'anuncio': False, 'sms': False}]  

        # Cria um HASH da senha.
        senha = data.senha
        hash_senha = motando_utils.create_hash(senha)   

        new_usuario = UsuarioParticularModelDb(**data.dict(), estado=estado, \
            estado_sigla=estado_sigla, cidade=cidade, telefone=telefone, \
            senha=hash_senha)
        
        nosql = NoSQL()
        added = nosql.add(data=new_usuario.dict(), table_name=NOSQL_TABLE_NAME)

        if added:
            return {'status': 'success', 'message': 'Usuário criado com sucesso.', 'code': 201}
        else:
            return {'status': 'error', 'message': 'Erro interno do servidor.', 'code': 500}
    
    def get_profile(self, email: str = None) -> dict:
        """Retorna dados do perfil do usuário.

        """
        global NOSQL_TABLE_NAME

        query = f'''
           SELECT email, email_confirmado, nome, perfil_img_url, telefone, cidade, 
               estado, estado_sigla, cep, endereco, anuncio_id, data_cadastro, data_modificacao
           FROM {NOSQL_TABLE_NAME} WHERE email = "{email}" LIMIT 1        
        '''

        nosql = NoSQL()
        nosql_result = nosql.query(query)

        if len(nosql_result) > 0:
            usuario_data = nosql_result[0]

            data_cadastro = usuario_data.get('data_cadastro')
            data_modificacao = usuario_data.get('data_modificacao')

            # Ajuste do objeto datetime para string.
            usuario_data['data_cadastro'] = data_cadastro.strftime('%d/%m/%Y %H:%M')
            usuario_data['data_modificacao'] = data_modificacao.strftime('%d/%m/%Y %H:%M')

            resp = {'status': 'success', 'data': [usuario_data], 'code': 200}                        
            
        else:
            resp = {'status': 'fail', 'message': 'Usuário não encontrado', 'code': 404}
        
        return resp








    
