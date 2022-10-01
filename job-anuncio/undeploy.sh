#!/bin/bash
#
# job-anuncio/deploy.sh
#

echo -e "[INFO] Undeploying JOB - ANUNCIO ...\n"

kubectl delete -f ./deployment.yaml

echo -e "\n[INFO] Undeploying Successful!" 
echo "[INFO] Exiting ..." 

exit 0