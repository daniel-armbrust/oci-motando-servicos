#!/bin/bash
#
# api-gateway/20220304/undeploy.sh
#

API_GATEWAY_NAME="gru_apigw-prd"
API_VERSION="20220304"
API_DEPLOY_NAME="api_$API_VERSION"
PATH_PREFIX="/motando/$API_VERSION"

echo -e "[INFO] Starting undeploy API GATEWAY ($API_GATEWAY_NAME) ..."

api_gateway_id="$(oci search resource structured-search \
    --query-text "query apigateway resources where displayName = \"$API_GATEWAY_NAME\"" \
    --query 'data.items[0].identifier' --raw-output)"

compartment_id="$(oci search resource structured-search \
    --query-text "query apigateway resources where displayName = \"$API_GATEWAY_NAME\"" \
    --query "data.items[0].\"compartment-id\"" --raw-output)"

if [ \( -z "$api_gateway_id" \) -o \( -z "$api_gateway_id" \) ]; then
   echo "[ERROR] Undeployment error. Could not continue."  
   echo "[ERROR] Exiting ..."
   exit 1
fi

deployment_id="$(oci api-gateway deployment list --all \
    --compartment-id "$compartment_id" --display-name "$API_DEPLOY_NAME" \
    --lifecycle-state "ACTIVE" --gateway-id "$api_gateway_id" \
    --query 'data.items[0].id' --raw-output)"

if [ -z "$deployment_id" ]; then
   echo "[ERROR] Undeployment error. Could not continue." 
   echo "[ERROR] Exiting ..."
   exit 1
fi

oci api-gateway deployment delete \
    --deployment-id "$deployment_id" \
    --force \
    --wait-for-state "SUCCEEDED"

if [ $? -ne 0 ]; then
   echo "[ERROR] Undeployment error."
   echo "[ERROR] Exiting ..."
   exit 1
else
   echo "[INFO] Undeployment Successful!" 
   echo "[INFO] Exiting ..." 
   exit 0
fi
