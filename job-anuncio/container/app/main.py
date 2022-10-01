#
# job-anuncio/container/app/main.py
#

import sys
from multiprocessing import Process

from modules.motando_anuncio import Anuncio


def publish_anuncio(anuncio_id: int = None):
    """Publica um anúncio.

    """
    anuncio = Anuncio()

    anuncio.publish(anuncio_id)


def process_anuncio(anuncio_id_list: tuple = None):
    """Inicia processamento para publicação dos anúncios.
    
    """
    proc_list = []

    for anuncio_id in anuncio_id_list:
        p = Process(target=publish_anuncio, args=(anuncio_id,))
        p.start()
        proc_list.append(p)
    
    if len(proc_list) > 0:
        for proc in proc_list:
            proc.join()
            
        proc_list = []
    

def main():
    """Execução principal.
    
    """
    anuncio = Anuncio()
    
    while True:
        # Obtém uma lista de anúncios não publicas
        anuncio_id_list = anuncio.get_nonpubsh_ids()

        if len(anuncio_id_list) > 0:
            process_anuncio(anuncio_id_list)
        else:
            break

    sys.exit(0)


if __name__ == '__main__':
    main()
else:
    sys.exit(1)