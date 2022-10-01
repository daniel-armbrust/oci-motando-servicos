#
# job-anuncio/container/app/modules/motando_anuncio.py
#

import os

from .motando_nosql import NoSQL
from .motando_objectstorage import ObjectStorage
from . import motando_utils

#
# Globals
#
NOSQL_TABLE_NAME = os.environ.get('MOTANDO_NOSQL_TABLE_NAME')
MAX_PARALLEL_ANUNCIO = os.environ.get('MAX_PARALLEL_ANUNCIO')


class Anuncio():
    def __init__(self):
        self.__offset = 0

    def __update_anuncio(self, anuncio_id: int, img_dict: dict):
        """Atualiza dados do anúncio.

        """
        global NOSQL_TABLE_NAME

        query = f'''
            UPDATE {NOSQL_TABLE_NAME} SET img_lista = {img_dict} WHERE id = {anuncio_id}
        '''

        nosql = NoSQL()
        nosql_result = nosql.query(query)

        if len(nosql_result) > 0:
            if nosql_result[0].get('NumRowsUpdated') != 1:
            # TODO: registrar evento de falha ao atualizar anúncio.
                pass

    def __workflow_move(self, email: str, img_dict: dict) -> dict:
        """Atividade de movimentação da imagem temporária para bucket permanente.
                
        """        
        tmp_img_filename = img_dict.get('tmp_img')

        randstr = motando_utils.return_randstr()

        src_img_path = f'{email}/{tmp_img_filename}'                
        dst_img_path = '%s%s' % (randstr, os.path.splitext(tmp_img_filename)[1])

        objectstorage = ObjectStorage()

        work_request_id = objectstorage.move(src_img_path, dst_img_path)

        if work_request_id:
            img_url = objectstorage.get_img_url(dst_img_path)

            img_dict.update({
                'status': 'MOVE', 'work_request_id': work_request_id, 'url': img_url
            })
        
        return img_dict
    
    def __workflow_delete(self, email: str, img_dict: dict) -> dict:
        """Atividade para excluír a imagem temporária do anúncio.

        """
        work_request_id = img_dict.get('work_request_id')

        if not work_request_id:
            return img_dict

        objectstorage = ObjectStorage()

        work_request_status = objectstorage.get_status(work_request_id)        

        if work_request_status == 'COMPLETED':
            tmp_img_filename = img_dict.get('tmp_img')

            img_path = f'{email}/{tmp_img_filename}'

            deleted = objectstorage.del_tmp_img(img_path)

            if deleted:
                img_dict.pop('tmp_img')
                img_dict.pop('work_request_id')                
                img_dict.update({'status': 'DONE'})
        
        return img_dict
    
    def __workflow_done(self, anuncio_id: int, img_dict: dict, moto_dict: dict) -> dict:
        """Atividades finais para publicar o anúncio.

        """
        global NOSQL_TABLE_NAME

        marca_id = moto_dict.get('marca_id')
        modelo_id = moto_dict.get('modelo_id')

        marca_data = motando_utils.get_moto_marca(marca_id)
        marca_nome = marca_data[0].get('marca')

        modelo_data = motando_utils.get_moto_modelo(marca_id, modelo_id)
        modelo_nome = modelo_data[0].get('modelo')

        query = f'''
           UPDATE {NOSQL_TABLE_NAME} SET moto_marca = "{marca_nome}", 
              moto_modelo = "{modelo_nome}", publicado = true 
           WHERE id = {anuncio_id}
        '''

        nosql = NoSQL()
        nosql_result = nosql.query(query)

        if len(nosql_result) > 0:
            if nosql_result[0].get('NumRowsUpdated') == 1:
                img_dict.pop('status')

        return img_dict        
   
    def get_anuncio(self, anuncio_id: int = None) -> dict:
        """Obtém somente algumas propriedades de um anúncio em particular
        (email e lista de imagens).
        
        """
        global NOSQL_TABLE_NAME

        query = f'''
            SELECT moto_marca, moto_modelo, email, img_lista FROM {NOSQL_TABLE_NAME} 
               WHERE id = {anuncio_id}
        '''

        nosql = NoSQL()
        nosql_result = nosql.query(query)
        
        if len(nosql_result) > 0:
            return nosql_result[0]
        else:
            return {}

    def get_nonpubsh_ids(self) -> tuple:
        """Retorna uma lista de IDs dos anúncios com status de não publicados.

        """
        global NOSQL_TABLE_NAME, MAX_PARALLEL_ANUNCIO

        query = f'''
          SELECT id FROM {NOSQL_TABLE_NAME} WHERE 
              publicado = false LIMIT {MAX_PARALLEL_ANUNCIO} OFFSET {self.__offset}
        '''

        self.__offset += int(MAX_PARALLEL_ANUNCIO)

        nosql = NoSQL()
        nosql_result = nosql.query(query)

        id_list = []

        for id_result in nosql_result:
            id_list.append(id_result.get('id'))
        
        return tuple(id_list) 

    def publish(self, anuncio_id: int = None):
        """Inicia workflow de publicação de anúncio.

        """
        anuncio = self.get_anuncio(anuncio_id)       

        email = anuncio.get('email')
        img_list = anuncio.get('img_lista')

        new_img_list = []

        for img_props in img_list:
            status = img_props.get('status')           

            if not status:
                new_props = self.__workflow_move(email, img_props)
            elif status == 'MOVE':
                new_props = self.__workflow_delete(email, img_props)   
            elif status == 'DONE':
                moto_marca_id = anuncio.get('moto_marca')
                moto_modelo_id = anuncio.get('moto_modelo')

                moto_props = {'marca_id': moto_marca_id, 'modelo_id': moto_modelo_id}

                new_props = self.__workflow_done(anuncio_id, img_props, moto_props)
            
            new_img_list.append(new_props)
        else:
            self.__update_anuncio(anuncio_id, new_img_list)