#
# auth/modules/motando_nosql.py
#

import sys
import logging

import oci

from borneo.iam import SignatureProvider
from borneo import NoSQLHandle, NoSQLHandleConfig, Regions, QueryRequest


class NoSQL():    
    def __init__(self, nosql_cmp: str = None):
        log = logging.getLogger(__name__)
        log_handler = logging.StreamHandler(sys.stdout)
        log_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        log_handler.setLevel(logging.WARNING)
        log.addHandler(log_handler)
        
        signer = oci.auth.signers.InstancePrincipalsSecurityTokenSigner()        
        region = signer.region

        provider = SignatureProvider(provider=signer)
        nosql_endpoint = Regions.from_region_id(region)

        handle_config = NoSQLHandleConfig(endpoint=nosql_endpoint, provider=provider)
        provider.close()

        handle_config.set_logger(log)
        handle_config.set_default_compartment(nosql_cmp)

        self.__nosql_handle = NoSQLHandle(handle_config)    

    def exec_query(self, query: str = None) -> list:
      """Execute a SQL Query.

      """
      query_request = QueryRequest()
      query_request.set_statement(query)
  
      nosql_result = []      

      while True:
          query_result = self.__nosql_handle.query(query_request)

          for result in query_result.get_results():
              nosql_result.append(result)

          if query_request.is_done():  
              break

      self.__nosql_handle.close()

      return nosql_result