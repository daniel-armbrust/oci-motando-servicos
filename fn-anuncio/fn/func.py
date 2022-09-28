#
# fn-anuncio/fn/func.py
#

import io
import json
import logging

from fdk import response

import oci


def handler(ctx, data: io.BytesIO = None):
    """Execução principal.
    
    """
    env_vars = dict(ctx.Config())
    
    bucket_anuncio = env_vars.get('ANUNCIO_BUCKET_NAME')
    bucket_img_src = env_vars.get('IMAGEM_TMP_BUCKET_NAME')
    bucket_tmp_anuncio = env_vars.get('ANUNCIO_TMP_BUCKET_NAME') 
        
    #try:
    event_body = json.loads(data.getvalue())
    #except (Exception, ValueError) as ex:
    #    logging.getLogger().info('error parsing json payload: ' + str(ex))
    
    print(event_body)
    logging.getLogger().debug(str(event_body))

    # 1 - Processar o arquivo JSON do BUCKET de Anuncio.
    #     ++ Chamadas internas as APIs.
    # 2 - Transportar as imagens temporárias do bucket temporário para o bucket de anuncios.
    # 3 - Inserir os registros do anuncio ao NoSQL.

