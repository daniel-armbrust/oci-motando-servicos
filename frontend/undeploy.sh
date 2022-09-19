#!/bin/bash
#
# frontend/undeploy.sh
#

LB_BACKENDSET_NAME="bckset-1_albpub-motando_prd"
LB_NAME="albpub-motando_prd"
CLUSTERIP_SERVICE_PORT=30080

function get_lb_ocid() {

   local lb_ocid=""
   local json_backendset=""

   lb_ocid="$(oci search resource structured-search \
      --query-text "query loadbalancer resources 
         where (displayName = '$LB_NAME' && lifeCycleState = 'ACTIVE')" \
      --query 'data.items[0].identifier' --raw-output)"
   
   echo -n "$lb_ocid"  
}

echo -e "[INFO] Undeploying Motando FRONTEND ...\n"

lb_ocid="$(get_lb_ocid)"

if [ -z "$lb_ocid" ]; then
   echo -e "\n[WARN] Could not find Load Balancer ($LB_NAME). The Backend Set ($LB_BACKENDSET_NAME) will not be touched ..." 
   echo "[WARN] Continuing ..."
else
   echo "[INFO] Removing Backend Set ($LB_BACKENDSET_NAME) entries ..."

   oci lb backend-set update \
       --load-balancer-id "$lb_ocid" \
       --backend-set-name "$LB_BACKENDSET_NAME" \
       --policy "ROUND_ROBIN" \
       --health-checker-protocol "TCP" \
       --health-checker-port "$CLUSTERIP_SERVICE_PORT" \
       --backends '[]' \
       --wait-for-state SUCCEEDED \
       --force 
fi

kubectl delete -f ./service.yaml
kubectl delete -f ./deployment.yaml

echo -e "\n[INFO] Undeploying Successful!" 
echo "[INFO] Exiting ..." 

exit 0