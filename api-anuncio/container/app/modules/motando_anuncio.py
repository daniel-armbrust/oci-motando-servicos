#
# modules/motando_anuncio.py
#

import os
import json

import oci

from .motando_models import AnuncioModel, AnuncioModelDb
from .motando_nosql import NoSQL
from . import motando_utils

#
# Globals
#
NOSQL_TABLE_NAME = os.environ.get('MOTANDO_NOSQL_TABLE_NAME')
BUCKET_IMGTMP_NAME = os.environ.get('MOTANDO_IMGTMP_BUCKET_NAME')
BUCKET_TMP_NAME = os.environ.get('MOTANDO_TMP_BUCKET_NAME')
BUCKET_NAME = os.environ.get('MOTANDO_BUCKET_NAME')


class Anuncio():
    def __init__(self):
        signer = oci.auth.signers.InstancePrincipalsSecurityTokenSigner()    
        
        region = signer.region

        self._client = oci.object_storage.ObjectStorageClient(config={'region': region}, signer=signer)
        self._objstg_ns = self._client.get_namespace().data
    
    @property
    def email(self) -> str:
        return self._email
    
    @email.setter
    def email(self, email: str = None):
        self._email = email
        

    def add(self, data: AnuncioModel) -> dict:
        """Adiciona um novo anúncio.

        """
        global BUCKET_TMP_NAME
              
        anuncio = AnuncioModelDb(**data.dict(), email=self._email)
        anuncio_json = json.dumps(anuncio.dict())

        randstr = motando_utils.return_random_string()
        filename = f'{randstr}.json'

        try:
            resp = self._client.put_object(namespace_name=self._objstg_ns, bucket_name=BUCKET_TMP_NAME,
                object_name=filename, put_object_body=anuncio_json, content_type='application/json')
        except oci.exceptions.ServiceError:
            return {'status': 'error', 'message': 'Erro interno do servidor.', 'code': 500}
        
        if resp.status == 200:
            msg = {'status': 'success', 'message': 'Anuncio aceito. Aguarde a sua criação.', 'code': 202}
        else:
            msg = {'status': 'error', 'message': 'Erro interno do servidor.', 'code': 500}
        
        return msg

    def add_img_tmp(self, filename: str = None, data: str = None) -> dict:
        """Salva temporariamente uma imagem em um BUCKET de uso temporário.
        
        """
        global BUCKET_IMGTMP_NAME

        img_filename = f'{self._email}/{filename}'

        mimetype = motando_utils.return_img_mimetype(img_filename)

        try:
            resp = self._client.put_object(namespace_name=self._objstg_ns, bucket_name=BUCKET_IMGTMP_NAME, 
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