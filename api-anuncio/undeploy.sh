#!/bin/bash
#
# anuncio/undeploy.sh
#

echo -e "[INFO] Undeploying API - ANUNCIO ...\n"

kubectl delete -f ./service.yaml
kubectl delete -f ./deployment.yaml

echo -e "\n[INFO] Undeploying Successful!" 
echo "[INFO] Exiting ..." 

exit 0