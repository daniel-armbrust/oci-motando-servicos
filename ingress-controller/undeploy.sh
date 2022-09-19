#!/bin/bash
#
# ingress-controller/undeploy.sh
#

echo -e "[INFO] Undeploying INGRESS-CONTROLLER ...\n"

    kubectl delete -f ./service.yaml
    kubectl delete -f ./deployment.yaml

echo -e "\n[INFO] Undeploying Successful!" 
echo "[INFO] Exiting ..." 

exit 0