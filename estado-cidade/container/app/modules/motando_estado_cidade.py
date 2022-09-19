#
# estado-cidade/modules/motando_estado_cidade.py
#
import json

import oci


class Estado():
    """Classe para obter os Estados brasileiros que estão contidos em arquivo
    JSON no Object Storage.

    """
    def __init__(self, region=None, objstg_ns=None, bucket_name=None):       
        # https://docs.oracle.com/en-us/iaas/Content/API/Concepts/sdk_authentication_methods.htm#sdk_authentication_methods_instance_principaldita 
        signer = oci.auth.signers.InstancePrincipalsSecurityTokenSigner()        
        self._client = oci.object_storage.ObjectStorageClient(config={'region': region}, signer=signer)

        self._objstg_ns = objstg_ns
        self._objstg_bucket = bucket_name

    def __get_objstg_filename(self, filename=None):
        """Retorna o conteúdo do arquivo armazenado no Object Storage.

        Args:
            filename: Nome do arquivo existente no Object Storage.

        """
        objstg_resp = None

        try:
            objstg_resp = self._client.get_object(self._objstg_ns, self._objstg_bucket, filename)
        except oci.exceptions.ServiceError as e:
            if e.status == 404:
                return {'status': 'fail', 'message': 'Not found.', 'code': 404}
            else:
                return {'status': 'error', 'message': 'Internal Server Error.', 'code': 500}

        if objstg_resp.status == 200:
            json_content = json.loads(objstg_resp.data.content)

            return json_content

        else:
            return {'status': 'error', 'message': 'Internal Server Error.', 'code': 500}

    def return_all(self):
        """Retorna um dicionário contendo todos os Estados e suas propriedades.
        Este dicionário é convertido a partir de um arquivo JSON obtido do 
        Object Storage. 

        """
        filename = 'estado.json'

        data = self.__get_objstg_filename(filename)
        data = dict(data)

        return data
    
    def return_by_id(self, estado_id=None):
        """Retorna as propriedades de um Estado em particular através do seu 
        identificador.

        Args:
            estado_id: Identificador numérico de um Estado.            

        """
        filename = f'{estado_id}/estado.json'

        data = self.__get_objstg_filename(filename)
        data = dict(data)

        return data


class Cidade():
    """Classe para obter as Cidades brasileiras que estão contidas em arquivo
    JSON no Object Storage.

    """
    def __init__(self, region=None, objstg_ns=None, bucket_name=None):       
        # https://docs.oracle.com/en-us/iaas/Content/API/Concepts/sdk_authentication_methods.htm#sdk_authentication_methods_instance_principaldita 
        signer = oci.auth.signers.InstancePrincipalsSecurityTokenSigner()        
        self._client = oci.object_storage.ObjectStorageClient(config={'region': region}, signer=signer)

        self._objstg_ns = objstg_ns
        self._objstg_bucket = bucket_name

    def __get_objstg_filename(self, filename=None):
        """Retorna o conteúdo do arquivo armazenado no Object Storage.

        Args:
            filename: Nome do arquivo existente no Object Storage.

        """
        objstg_resp = None

        try:
            objstg_resp = self._client.get_object(self._objstg_ns, self._objstg_bucket, filename)
        except oci.exceptions.ServiceError as e:
            if e.status == 404:
                return {'status': 'fail', 'message': 'Not found.', 'code': 404}
            else:
                return {'status': 'error', 'message': 'Internal Server Error.', 'code': 500}

        if objstg_resp.status == 200:
            json_content = json.loads(objstg_resp.data.content)

            return json_content

        else:
            return {'status': 'error', 'message': 'Internal Server Error.', 'code': 500}
    
    def return_all(self, estado_id=None):
        """Retorna todas as Cidades pertencentes a um Estado em particular.

        Args:
            estado_id: ID de um Estado.
        
        """
        filename = f'{estado_id}/cidade/cidade.json'

        data = self.__get_objstg_filename(filename)
        data = dict(data)

        return data
    
    def return_by_id(self, estado_id=None, cidade_id=None):
        """Retorna as propriedades de uma Cidade em particular pertencente a um
        Estado em particular.

        Args:
            estado_id: Identificador numérico de um Estado.
            cidade_id: Identificador numérico de uma Cidade.

        """
        filename = f'{estado_id}/cidade/{cidade_id}/cidade.json'

        data = self.__get_objstg_filename(filename)
        data = dict(data)

        return data