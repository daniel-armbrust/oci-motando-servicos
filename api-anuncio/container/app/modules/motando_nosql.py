#
# modules/motando_nosql.py
#

import os
import sys
import logging

import oci

from borneo.iam import SignatureProvider
from borneo import NoSQLHandle, NoSQLHandleConfig, Regions, QueryRequest
from borneo import PutRequest, PutOption

#
# Globals
#
NOSQL_CMP = os.environ.get('MOTANDO_NOSQL_CMP')
NOSQL_TABLE_NAME = os.environ.get('MOTANDO_NOSQL_TABLE_NAME')


class NoSQL():    
    def __init__(self):
        global NOSQL_CMP

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
        handle_config.set_default_compartment(NOSQL_CMP)

        self.__nosql_handle = NoSQLHandle(handle_config)
  
    def add(self, data=None): 
        global NOSQL_TABLE_NAME

        put_request = PutRequest()
        put_request.set_table_name(NOSQL_TABLE_NAME)
        put_request.set_option(PutOption.IF_ABSENT)
        put_request.set_value(data)

        result = self.__nosql_handle.put(put_request)
        self.__nosql_handle.close()

        if result.get_version() is not None:
            return True
        else:
            # TODO: registrar falha na inserção dos dados.
            return False
    
    def update(self, data: dict = None) -> bool:
        global NOSQL_TABLE_NAME

        put_request = PutRequest()
        put_request.set_table_name(NOSQL_TABLE_NAME)
        put_request.set_option(PutOption.IF_PRESENT)
        put_request.set_value(data)

        result = self.__nosql_handle.put(put_request)
        self.__nosql_handle.close()        

        if result.get_version() is not None:
            return True
        else:
            # TODO: registrar falha na inserção dos dados.
            return False

    def query(self, query: str = None) -> list:
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
