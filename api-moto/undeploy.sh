#!/bin/bash
#
# moto/undeploy.sh
#

OBJSTR_NAMESPACE="$(oci os ns get --query 'data' --raw-output)"
BUCKET_NAME="motando_moto"

echo -e "[INFO] Undeploying API - MOTO ...\n"

kubectl delete -f ./service.yaml
kubectl delete -f ./deployment.yaml

echo -e "\n[INFO] Deleting data from Object Storage (Bucket: $BUCKET_NAME) ..."

oci os object bulk-delete \
    --bucket-name "$BUCKET_NAME" \
    --namespace "$OBJSTR_NAMESPACE" \
    --force

echo -e "\n[INFO] Undeploying Successful!" 
echo "[INFO] Exiting ..." 

exit 0