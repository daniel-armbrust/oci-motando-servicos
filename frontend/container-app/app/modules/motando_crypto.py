#
# frontend/container-app/app/modules/motando_crypto.py
#

import os
import base64

import oci

#
# Globals
#
CRYPTO_ENDPOINT = os.environ.get('MOTANDO_CRYPTO_ENDPOINT')
MKE_ID = os.environ.get('MOTANDO_MKE_ID')


class MontadoCrypto():
    def __init__(self):
        global CRYPTO_ENDPOINT

        signer = oci.auth.signers.InstancePrincipalsSecurityTokenSigner()        
        region = signer.region

        # AES_256_GCM, RSA_OAEP_SHA_1, RSA_OAEP_SHA_256 
        self._encrypt_algo = 'RSA_OAEP_SHA_1'

        # ECDSA_SHA_256, ECDSA_SHA_384, ECDSA_SHA_512, SHA_224_RSA_PKCS1_V1_5,
        # SHA_224_RSA_PKCS_PSS, SHA_256_RSA_PKCS1_V1_5, SHA_256_RSA_PKCS_PSS,
        # SHA_384_RSA_PKCS1_V1_5, SHA_384_RSA_PKCS_PSS, SHA_512_RSA_PKCS1_V1_5,
        # SHA_512_RSA_PKCS_PSS
        self._sign_algo = 'SHA_256_RSA_PKCS_PSS'

        self._client = oci.key_management.KmsCryptoClient(signer=signer, 
            config={'region': region}, service_endpoint=CRYPTO_ENDPOINT)
    
    def encrypt(self, message: str = None) -> str:
        """Criptografa a mensagem informada como parâmetro através do seviço KMS
        do OCI.

        Returns:
            Retorna uma string no formato BASE64 contendo a mensagem criptografada.        
        """
        global MKE_ID

        # A mensagem deve ser convertida para BASE64 antes da criptografia.
        message_base64 = base64.b64encode(message.encode('utf-8')).decode()
      
        crypt_details = oci.key_management.models.EncryptDataDetails(key_id=MKE_ID,
          plaintext=message_base64)      

        try:
            resp = self._client.encrypt(encrypt_data_details=crypt_details)
        except oci.exceptions.ServiceError:
            return None
         
        if resp.status == 200:
            return resp.data.ciphertext
        else:
            return None
    
    def decrypt(self, crypt_message: str = None) -> str:
        """Descriptografa a mensagem informada como parâmetro através do seviço KMS
        do OCI.

        Returns:
            Retorna uma string já decodificada (BASE64).
        """
        global MKE_ID

        decrypt_details = oci.key_management.models.DecryptDataDetails(key_id=MKE_ID,
           ciphertext=crypt_message)
        
        try:
            resp = self._client.decrypt(decrypt_data_details=decrypt_details) 
        except oci.exceptions.ServiceError:            
            return None

        if resp.status == 200:
            message = base64.b64decode(resp.data.plaintext).decode()

            return message
        else:
            return None
    
    def sign(self, message: str = None) -> str:
        """Realiza o processo de assinatura digital sobre a mensagem informada
        como parâmetro através do serviço KMS do OCI.

        Returns:
            Retorna uma string BASE64 contendo a assinatura digital gerada.
        """
        global MKE_ID

        sign_details = oci.key_management.models.SignDataDetails(key_id=MKE_ID,          
            message=message, signing_algorithm=self._sign_algo)
        
        try:
            resp = self._client.sign(sign_data_details=sign_details)
        except oci.exceptions.ServiceError:
            return None
        
        if resp.status == 200:
            return resp.data.signature
        else:
            return None
    
    def is_valid_sign(self, message: str, sign: str) -> bool:
        """Verifica se a assinatura digital sobre a mensagem é válida.

        Return:
            Retorna True caso a assinatura digital seja válida ou False caso
        contrário.
        """
        global MKE_ID

        verify_sign_details = oci.key_management.models.VerifyDataDetails(key_id=MKE_ID,
            message=message, signature=sign, signing_algorithm=self._sign_algo)
        
        try:
            resp = self._client.sign(sign_data_details=verify_sign_details)
        except oci.exceptions.ServiceError:
            return None
        
        if resp.status == 200:
            if resp.data.is_signature_valid is True:           
               return True
            else:
               return False
        else:
            return None