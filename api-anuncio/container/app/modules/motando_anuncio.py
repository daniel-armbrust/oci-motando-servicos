#
# modules/motando_anuncio.py
#

import os
#import secrets
#from datetime import datetime

import oci

from .motando_models import AnuncioModel, AnuncioModelDb
from .motando_nosql import NoSQL
from . import motando_utils

#
# Globals
#
BUCKET_IMGTMP_NAME = os.environ.get('MOTANDO_IMGTMP_BUCKET_NAME')


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

        #randstr = secrets.token_hex(10) + datetime.now().strftime('%s')
        
        img_filename = f'{self._email}/{filename}'
        #img_filename = '%s/%s%s' % (self._email, randstr, os.path.splitext(filename)[1])

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