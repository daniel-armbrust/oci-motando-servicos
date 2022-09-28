#!/bin/bash
#
# fn-anuncio/deploy.sh
#

COMPARTMENT_NAME="cmp-motando"
BUCKET_NAME="motando_anuncio_tmp"

CONTEXT_NAME="motando-ctx"
FN_URL="https://functions.sa-saopaulo-1.oci.oraclecloud.com"
FN_APPL_NAME="motando-appl-fn_prd"
FN_NAME="$(cat fn/func.yaml | grep 'name:' | cut -f2 -d' ')"
RULE_NAME="rule-motando-anuncio"

OCIR_ENDPOINT="gru.ocir.io"
REPO_NAME="motando-fn"
OBJSTR_NAMESPACE="$(oci os ns get --query 'data' --raw-output)"

DOCKER_IMG_VERSION="1.0"
DOCKER_IMG_NAME="motando-fn-anuncio"
OCIR_IMG_NAME="$OCIR_ENDPOINT/$OBJSTR_NAMESPACE/$DOCKER_IMG_NAME"

function get_cmp_id() {

   local cmp_ocid=""

   cmp_ocid="$(oci search resource structured-search \
      --query-text "query compartment resources where displayName='$COMPARTMENT_NAME'" \
      --query 'data.items[0].identifier' --raw-output)"

   echo -n "$cmp_ocid" 
}

function get_bucket_id() {

   local bucket_ocid=""

   bucket_ocid="$(oci search resource structured-search \
      --query-text "query bucket resources where displayName='$BUCKET_NAME'" \
      --query 'data.items[0].identifier' --raw-output)"
    
   echo -n "$bucket_ocid"
}

function create_ctx() {
    
    local cmp_id="$(get_cmp_id)"

    echo -e "[INFO] Setup OCI-Function Context ...\n"

    fn inspect ctx "$CONTEXT_NAME" 2>/dev/null

    if [ $? -ne 0 ]; then

       fn create context "$CONTEXT_NAME" --provider oracle
       fn use context "$CONTEXT_NAME"

       fn update context oracle.compartment-id "$COMPARTMENT_ID"
       fn update context api-url "$FN_URL"
       fn update context registry "$OCIR_ENDPOINT/$OBJSTR_NAMESPACE/$REPO_NAME"
       fn update context oracle.image-compartment-id "$cmp_id"

    else
       fn use context "$CONTEXT_NAME"
    fi

    echo ""
}

function build_push() {       

    local current_dir="$(pwd)"

    echo -e "[INFO] Building and Pushing the docker image to OCIR ...\n"

    cd fn/

    fn deploy -v --no-cache --no-bump --app "$FN_APPL_NAME"    

    cd "$current_dir"

    echo ""
}

function create_event_rule() {
    
    local cmp_id="$(get_cmp_id)"
    local bucket_id="$(get_bucket_id)"

    local fn_id="$(fn list funcs "$FN_APPL_NAME" | grep "^$FN_NAME" | awk '{print $3}')"    
   
    oci events rule create \
        --compartment-id "$cmp_id" \
        --condition "{
                \"eventType\":[\"com.oraclecloud.objectstorage.createobject\"],
                \"data\":{\"additionalDetails\": {\"bucketId\":[\"$bucket_id\"]}}
             }" \
        --display-name "$RULE_NAME" \
        --is-enabled true \
        --actions "{
            \"actions\": [
                   {\"actionType\": \"FAAS\", \"description\": \"Evento - Motando Anúncio\", \"functionId\": \"$fn_id\"}
            ]}" \
        --wait-for-state "ACTIVE"
}

function deploy() {

    echo -e "[INFO] Starting deploy FUNCTION ($FN_APPL_NAME/$FN_NAME) ...\n"

    create_ctx
    build_push   
    create_event_rule

    fn use context default

    echo -e "\n[INFO] Deployment Successful!" 
    echo "[INFO] Exiting ..."
}

case $1 in    
      *)           
           deploy                                 
           ;;
esac

exit 0
