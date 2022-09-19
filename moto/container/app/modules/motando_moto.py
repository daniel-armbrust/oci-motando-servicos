#
# moto/modules/motando_moto.py
#
import json

import oci


class Moto():
    def __init__(self, region=None, objstg_ns=None, bucket_name=None):       
        # https://docs.oracle.com/en-us/iaas/Content/API/Concepts/sdk_authentication_methods.htm#sdk_authentication_methods_instance_principaldita 
        signer = oci.auth.signers.InstancePrincipalsSecurityTokenSigner()        
        self._client = oci.object_storage.ObjectStorageClient(config={'region': region}, signer=signer)

        self._objstg_ns = objstg_ns
        self._objstg_bucket = bucket_name

    def _get_objstg_filename(self, filename=None):
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


class Marca(Moto):
    """Classe para obter as Marcas de motos que estão contidas em arquivo JSON 
    no Object Storage.

    """
    def __init__(self, region=None, objstg_ns=None, bucket_name=None):
        Moto.__init__(self, region, objstg_ns, bucket_name)

    def return_all(self):
        """Retorna um dicionário contendo todas as Marcas de moto e suas 
        propriedades. Este dicionário é convertido a partir de um arquivo JSON 
        obtido do Object Storage. 

        """
        filename = 'marca.json'

        data = self._get_objstg_filename(filename)
        data = dict(data)

        return data
    
    def return_by_id(self, marca_id=None):
        """Retorna as propriedades de uma Marca de moto em particular.

        Args:
            marca_id: Identificador numérico de uma Marca de moto.            

        """
        filename = f'{marca_id}/marca.json'

        data = self._get_objstg_filename(filename)
        data = dict(data)

        return data


class Modelo(Moto):
    """Classe para obter os Modelos de uma Marca de motos que estão contidas em
    arquivo JSON no Object Storage.

    """
    def __init__(self, region=None, objstg_ns=None, bucket_name=None):
        Moto.__init__(self, region, objstg_ns, bucket_name)

    def return_all(self, marca_id=None):
        """Retorna um dicionário contendo todos os Modelos e suas propriedades 
        de uma Marca de moto. Este dicionário é convertido a partir de um arquivo 
        JSON obtido do Object Storage. 

        Args:
            marca_id: Identificador numérico de uma Marca de moto.

        """
        filename = f'{marca_id}/modelo/modelo.json'

        data = self._get_objstg_filename(filename)
        data = dict(data)

        return data
    
    def return_by_id(self, marca_id=None, modelo_id=None):
        """Retorna as propriedades de um Modelo de uma Marca de moto em 
        particular.

        Args:
            marca_id: Identificador numérico de uma Marca de moto.     
            modelo_id: Identificador numérico de um Modelo pertencente a 
        uma Marca.

        """
        filename = f'{marca_id}/modelo/{modelo_id}/modelo.json'

        data = self._get_objstg_filename(filename)
        data = dict(data)

        return data


class Versao(Moto):
    """Classe para obter as Versões dos Modelos de uma Marca de motos que estão
    contidas em arquivo JSON no Object Storage.

    """   
    def __init__(self, region=None, objstg_ns=None, bucket_name=None):
        Moto.__init__(self, region, objstg_ns, bucket_name)

    def return_all(self, marca_id=None, modelo_id=None):
        """Retorna um dicionário contendo todas as Versões e suas propriedades 
        referente a um Modelo de uma Marca de moto. Este dicionário é convertido 
        a partir de um arquivo JSON obtido do Object Storage. 

        Args:
            marca_id: Identificador numérico de uma Marca de moto.
            modelo_id: Identificador numérico de um Modelo pertencente a 
        uma Marca.

        """
        filename = f'{marca_id}/modelo/{modelo_id}/versao/versao.json'

        data = self._get_objstg_filename(filename)
        data = dict(data)

        return data
    
    def return_by_id(self, marca_id=None, modelo_id=None, versao_id=None):
        """Retorna um dicionário contendo as propriedades de uma Versão referente
        a um Modelo de uma Marca de moto. Este dicionário é convertido a partir 
        de um arquivo JSON obtido do Object Storage. 

        Args:
            marca_id: Identificador numérico de uma Marca de moto.
            modelo_id: Identificador numérico de um Modelo pertencente a 
        uma Marca.
            versao_id: Identificador numérico de uma Versão pertencente a
        um Modelo.

        """
        filename = f'{marca_id}/modelo/{modelo_id}/versao/{versao_id}/versao.json'

        data = self._get_objstg_filename(filename)
        data = dict(data)

        return data