#
# modules/motando_anuncio.py
#

import os

import oci

from .motando_models import AnuncioModel, AnuncioModelList
from .motando_models import AnuncioModelDb, AnuncioModelDbUpdate, AnuncioModelDbOut
from .motando_nosql import NoSQL
from . import motando_utils

#
# Globals
#
BUCKET_IMGTMP_NAME = os.environ.get('MOTANDO_IMGTMP_BUCKET_NAME')
NOSQL_TABLE_NAME = os.environ.get('MOTANDO_NOSQL_TABLE_NAME')


class Anuncio():
    def __init__(self):
        signer = oci.auth.signers.InstancePrincipalsSecurityTokenSigner()    
        
        region = signer.region

        self._objstg_client = oci.object_storage.ObjectStorageClient(config={'region': region}, signer=signer)
        self._objstg_ns = self._objstg_client.get_namespace().data
        
    @property
    def email(self) -> str:
        return self._email
    
    @email.setter
    def email(self, email: str = None):
        self._email = email        

    def get(self, anuncio_id: int) -> dict:
        """Retorna um anúncio em particular.

        """
        global NOSQL_TABLE_NAME

        query = f'''
            SELECT id, moto_marca, moto_modelo, ano_fabricacao, ano_modelo, placa, 
                   km, zero_km, cor, preco, frase_vendedora, descricao, opcional_alarme,
                   opcional_bau, opcional_computador, opcional_gps, aceita_contraoferta,
                   aceita_troca, doc_ok, sinistro, trilha_pista, freios, tipo_partida,
                   refrigeracao, estilo, origem, m.img_lista.url AS img_lista
              FROM {NOSQL_TABLE_NAME} m WHERE email = "{self._email}" AND 
                 (publicado = true AND id = {anuncio_id})
        '''

        nosql = NoSQL()
        nosql_result = nosql.query(query)

        if len(nosql_result) > 0:
            anuncio = AnuncioModelDbOut(**nosql_result[0])

            anuncio_json = anuncio.json()
            
            return {'status': 'success', 'data': anuncio_json, 'code': 200}
        else:
            return {'status': 'fail', 'message': 'Nenhum anúncio encontrado.', 'code': 404}
    
    def get_total(self) -> dict:
        """Obtém o total de anúncios "publicados" e "não publicados".

        """
        global NOSQL_TABLE_NAME

        query_publicado = f''' 
            SELECT count(id) as publicado FROM {NOSQL_TABLE_NAME} 
               WHERE email = "{self._email}" AND publicado = true
        '''      

        nosql = NoSQL()
        nosql_result_publicado = nosql.query(query_publicado)

        if len(nosql_result_publicado) > 0:
            count_publicado = nosql_result_publicado[0]['publicado']
        else:
            count_publicado = 0

        query_nao_publicado = f''' 
            SELECT count(id) as nao_publicado FROM {NOSQL_TABLE_NAME} 
               WHERE email = "{self._email}" AND publicado = false
        '''

        nosql = NoSQL()
        nosql_result_nao_publicado = nosql.query(query_nao_publicado)       

        if len(nosql_result_nao_publicado) > 0:
            count_nao_publicado = nosql_result_nao_publicado[0]['nao_publicado']
        else:
            count_nao_publicado = 0
        
        data = {'total_publicado': count_publicado, 'total_nao_publicado': count_nao_publicado}

        return {'status': 'success', 'data': data, 'code': 200}
    
    def list(self, offset: int = 0) -> dict:
        """Lista os anúncios de determinado usuário (particular ou lojista).
        
        """
        global NOSQL_TABLE_NAME

        limit = 10

        if offset < 0:
            offset = 0
        
        query = f'''
            SELECT id, moto_marca, moto_modelo, ano_fabricacao, ano_modelo, km, 
                   zero_km, cor, preco, publicado, vendido, img_lista, data_cadastro 
                FROM {NOSQL_TABLE_NAME} 
            WHERE email = "{self._email}" LIMIT {limit} OFFSET {offset}
        '''

        nosql = NoSQL()
        nosql_result = nosql.query(query)

        if len(nosql_result) > 0:
            anuncio_list = []

            for result in nosql_result:
                db_preco = result.pop('preco')
                preco = '{:.2f}'.format(db_preco)

                db_data_cadastro = result.pop('data_cadastro')
                data_cadastro = db_data_cadastro.strftime('%d/%m/%Y')

                db_img_lista = result.pop('img_lista')

                if result.get('publicado') == True:
                    img_lista = []

                    for img_url in db_img_lista:
                        img_lista.append(img_url.get('url'))
                    
                    result.update({'status': 'publicado', 'preco': preco, 
                        'data_cadastro': data_cadastro, 'img_lista': img_lista})         
                else:
                    result.update({'status': 'aguardando publicação', 'preco': preco, 
                        'data_cadastro': data_cadastro})
                
                anuncio = AnuncioModelList.parse_obj(result)
                anuncio_list.append(anuncio.dict())
            
            # Obtém o total de anúncios publicados e não publicados.
            data_total = self.get_total()
            
            return {'status': 'success', 'data': anuncio_list, 'meta': data_total.get('data'), 'code': 200}

        else:
            return {'status': 'fail', 'message': 'Nenhum anúncio encontrado.', 'code': 404}

    def add(self, data: AnuncioModel) -> dict:
        """Adiciona um novo anúncio.

        """     
        anuncio_dict = data.dict()   

        img_lista = anuncio_dict.pop('img_lista')

        new_img_lista = []

        # Cria uma nova lista de imagens para processamento futuro.
        for img in img_lista:
            img_props = {'url' : '', 'tmp_img': img, 'work_request_id': '', 'status': ''}
            new_img_lista.append(img_props)            

        # Prepara novo anúncio para ser adicionado e publicado futuramente.
        anuncio_dict.update({'email': self._email})        
        anuncio_dict.update({'img_lista': new_img_lista})  

        anuncio = AnuncioModelDb.parse_obj(anuncio_dict)
        
        nosql = NoSQL()
        added = nosql.add(anuncio.dict())       

        if added:
            return {'status': 'success', 'message': 'Anuncio aceito. Aguarde a sua criação.', 'code': 202}
        else:
            return {'status': 'error', 'message': 'Erro interno do servidor.', 'code': 500}               

    def add_img_tmp(self, filename: str = None, data: str = None) -> dict:
        """Salva temporariamente uma imagem em um BUCKET de uso temporário.
        
        """
        global BUCKET_IMGTMP_NAME        
        
        img_filename = f'{self._email}/{filename}'
        
        mimetype = motando_utils.return_img_mimetype(img_filename)

        try:
            resp = self._objstg_client.put_object(namespace_name=self._objstg_ns, bucket_name=BUCKET_IMGTMP_NAME, 
                object_name=img_filename, put_object_body=data, content_type=mimetype)
        except oci.exceptions.ServiceError:
            return {'status': 'error', 'message': 'Erro interno do servidor.', 'code': 500}
        
        if resp.status == 200:
            msg = {'status': 'success', 'message': 'Imagem salva com sucesso.', 
               'data': [{'filename': img_filename}], 'code': 201}
        else:
            msg = {'status': 'error', 'message': 'Erro interno do servidor.', 'code': 500}
        
        return msg

    def del_img_tmp(self):
        global BUCKET_IMGTMP_NAME    
    
    def update(self, anuncio_id: int, data: AnuncioModel) -> dict:
        """ 

        """
        anuncio_dict = data.dict()

        anuncio_dict.update({'id': anuncio_id})

        print('Anuncio DICT')
        print(anuncio_dict)

        img_lista = anuncio_dict.pop('img_lista')

        anuncio_dict.update({'email': self._email})
        anuncio_dict.update({'img_lista': []})

        anuncio = AnuncioModelDbUpdate.parse_obj(anuncio_dict)

        print('Anuncio Obj')
        print(anuncio)

        nosql = NoSQL()
        updated = nosql.update(anuncio.dict())       

        if updated:
            return {'status': 'success', 'message': 'Atualização aceita. Aguarde a sua finalização.', 'code': 202}
        else:
            return {'status': 'error', 'message': 'Erro interno do servidor.', 'code': 500}               


class AnuncioPublico():
    pass