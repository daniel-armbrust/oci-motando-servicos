#
# modules/motando_authjwt.py
#

import os
import base64
from datetime import datetime

import oci
from fastapi import HTTPException, status
from jose import jwt, JWTError

#
# Globals
#
JWT_SECRETKEY_ID = os.environ.get('MOTANDO_CSRF_SECRETKEY_ID')


class MotandoAuthJwt():
    def __init__(self):
        signer = oci.auth.signers.InstancePrincipalsSecurityTokenSigner()

        region = signer.region

        self.__client = oci.secrets.SecretsClient(config={'region': region}, signer=signer)

    def __get_secret_key(self) -> str:
        """Obtém o SECRET_KEY a partir do serviço OCI Vault que será usado para 
        assinar o Token JWT.
        
        """
        global JWT_SECRETKEY_ID
       
        try:
            resp = self.__client.get_secret_bundle(secret_id=JWT_SECRETKEY_ID, stage='LATEST')
        except oci.exceptions.ServiceError:
            return None

        if resp.status == 200:
            base64_content = resp.data.secret_bundle_content.content
            txt_decoded = base64.b64decode(base64_content).decode()

            return txt_decoded

        else:
            return None
        
    def verify_token(self, token: str = None) -> dict:
        """Verifica o JWT Token informado como parâmetro.

        """
        secret_key = self.__get_secret_key()

        if not secret_key:
            # TODO: registrar evento de erro.
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail='Erro interno do servidor.'
            )

        try:
            token_payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        except JWTError:
            msg = {''}
            # TODO: registrar evento de erro.
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail='Token inválido.'
            )
        
        token_expires = token_payload.get('expires')

        if datetime.now() > datetime.utcfromtimestamp(token_expires):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Token expirado.'
            )
        else:
            return token_payload       