#
# job-anuncio/container/app/modules/motando_objectstorage.py
#

import os
import sys

import oci

#
# Globals
#
BUCKET_NAME = os.environ.get('MOTANDO_ANUNCIO_BUCKET_NAME')
BUCKET_IMGTMP_NAME = os.environ.get('MOTANDO_IMGTMP_BUCKET_NAME')


class ObjectStorage():
    def __init__(self):
        signer = oci.auth.signers.InstancePrincipalsSecurityTokenSigner()    
        
        self._region = signer.region

        self._objstg_client = oci.object_storage.ObjectStorageClient(config={'region': self._region}, signer=signer)
        self._objstg_ns = self._objstg_client.get_namespace().data

        self._objstg_service_url = f'https://objectstorage.{self._region}.oraclecloud.com'
    
    def move(self, src_img_path: str, dst_img_path: str) -> str:
        """Move imagem da origem presente no bucket temporário para seu destino
        em um bucket permanente.

        Returns:
            Retorna o Work Request ID da operação que foi realizada.

        """
        global BUCKET_NAME, BUCKET_IMGTMP_NAME        
       
        copy_details = oci.object_storage.models.CopyObjectDetails(
            source_object_name=src_img_path, destination_object_name=dst_img_path,
            destination_bucket=BUCKET_NAME, destination_region=self._region,
            destination_namespace=self._objstg_ns)

        try:
            resp = self._objstg_client.copy_object(namespace_name=self._objstg_ns, 
                bucket_name=BUCKET_IMGTMP_NAME, copy_object_details=copy_details)
        except oci.exceptions.ServiceError as e:
            # TODO: registrar falha.
            sys.stderr.write(e + '\n')
            return None        

        # Verifica se a atividade de copia entre buckets foi aceita.
        if resp.status == 202:
            return resp.headers.get('opc-work-request-id')
        else:
            return None
    
    def del_tmp_img(self, img_path: str) -> bool:
        """Excluí imagem presente em bucket temporário.
        
        """
        global BUCKET_IMGTMP_NAME

        try:
            resp = self._objstg_client.delete_object(namespace_name=self._objstg_ns, 
                bucket_name=BUCKET_IMGTMP_NAME, object_name=img_path)
        except oci.exceptions.ServiceError as e:
            # TODO: registrar falha.
            sys.stderr.write(e + '\n')
            return False       

        # Verifica se a atividade de copia entre buckets foi aceita.
        if resp.status == 204:
            return True
        else:
            return False
    
    def get_status(self, work_request_id: str = None) -> str:
        """Retorna o status do Work Request através do seu ID.

        """
        try:
            resp = self._objstg_client.get_work_request(work_request_id=work_request_id)
        except oci.exceptions.ServiceError as e:
            sys.stderr.write(e + '\n')
            return None
        else:
            return resp.data.status
    
    def get_img_url(self, img_path: str) -> str:
        """Obtém a URL da imagem.

        """
        global BUCKET_NAME

        url = f'{self._objstg_service_url}/n/{self._objstg_ns}/b/{BUCKET_NAME}/o/{img_path}'

        return url