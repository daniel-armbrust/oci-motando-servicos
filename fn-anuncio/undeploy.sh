#!/bin/bash
#
# fn-anuncio/undeploy.sh
#

COMPARTMENT_NAME="cmp-motando"

CONTEXT_NAME="motando-ctx"

FN_APPL_NAME="motando-appl-fn_prd"
FN_NAME="$(cat fn/func.yaml | grep 'name:' | cut -f2 -d' ')"
RULE_NAME="rule-motando-anuncio"

function get_cmp_id() {

   local cmp_ocid=""

   cmp_ocid="$(oci search resource structured-search \
      --query-text "query compartment resources where displayName='$COMPARTMENT_NAME'" \
      --query 'data.items[0].identifier' --raw-output)"

   echo -n "$cmp_ocid" 
}

echo -e "[INFO] Undeploying FUNCTION ($FN_APPL_NAME/$FN_NAME) ...\n"

cmp_id="$(get_cmp_id)"

event_id="$(oci events rule list --compartment-id "$cmp_id" \
    --display-name "$RULE_NAME" --lifecycle-state "ACTIVE" \
    --query "data[0].id" --raw-output)"

oci events rule delete --rule-id "$event_id" --force --wait-for-state "DELETED"

fn use context "$CONTEXT_NAME"

fn_id="$(fn list funcs "$FN_APPL_NAME" | grep "^$FN_NAME" | awk '{print $3}')"

fn use context default

oci fn function delete --function-id "$fn_id" --force --wait-for-state "DELETED"

echo -e "\n[INFO] Undeploying Successful!" 
echo "[INFO] Exiting ..." 

exit 0