#!/bin/bash
#
# api-gateway/20220304/deploy.sh
#

API_GATEWAY_NAME="gru_apigw-prd"
API_VERSION="20220304"
API_DEPLOY_NAME="api_$API_VERSION"
PATH_PREFIX="/motando/$API_VERSION"

function get_compartment_id() {

    local compartment_id="$(oci search resource structured-search \
       --query-text "query apigateway resources where displayName = \"$API_GATEWAY_NAME\"" \
       --query "data.items[0].\"compartment-id\"" --raw-output)"   

    echo -n "$compartment_id"
}

function get_apigateway_id() {

   local apigateway_id="$(oci search resource structured-search \
      --query-text "query apigateway resources where displayName = \"$API_GATEWAY_NAME\"" \
      --query 'data.items[0].identifier' --raw-output)"
   
   echo -n "$apigateway_id"
}

function get_deployment_id() {

   local deployment_id=""
   
   local compartment_id="$(get_compartment_id)"
   local apigateway_id="$(get_apigateway_id)"     

   deployment_id="$(oci api-gateway deployment list --all \
      --compartment-id "$compartment_id" \
      --gateway-id "$apigateway_id" \
      --display-name "$API_DEPLOY_NAME" \
      --lifecycle-state "ACTIVE" \
      --query 'data.items[0].id' --raw-output 2>/dev/null)"

   echo -n "$deployment_id"  
}

function deploy() {

    local compartment_id=""
    local apigateway_id=""
    local deployment_id=""

    echo "[INFO] Starting deploy API GATEWAY ($API_GATEWAY_NAME) ..."

    deployment_id="$(get_deployment_id)"    

    if [ ! -z "$deployment_id" ]; then
       echo "[WARN] The deployment \"$API_DEPLOY_NAME\" from API GATEWAY \"$API_GATEWAY_NAME\" already exists." 
       echo "[WARN] Exiting ..."
       exit 0
    fi    

    compartment_id="$(get_compartment_id)"
    apigateway_id="$(get_apigateway_id)"

    if [ \( -z "$compartment_id" \) -o \( -z "$apigateway_id" \) ]; then
       echo "[ERROR] Deployment error. Could not continue." 
       echo "[ERROR] Exiting ..."
       exit 1
    fi    

    oci api-gateway deployment create \
      --compartment-id "$compartment_id" \
      --gateway-id "$apigateway_id" \
      --path-prefix "$PATH_PREFIX" \
      --display-name "$API_DEPLOY_NAME" \
      --wait-for-state "SUCCEEDED" \
      --specification "file://api-specification.json"

    if [ $? -ne 0 ]; then
       echo "[ERROR] Deployment error."
       echo "[ERROR] Exiting ..."
       exit 1
    else
       echo "[INFO] Deployment Successful!" 
       echo "[INFO] Exiting ..."       
    fi
}

case $1 in
    -dp-id|--dp-id|--get-deployment-id)
        echo "$(get_deployment_id)"
        ;;
    *)
       deploy       
       ;;
esac

exit 0