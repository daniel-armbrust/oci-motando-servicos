#!/bin/bash
#
# moto/deploy.sh
#

OCIR_ENDPOINT="gru.ocir.io"
OBJSTR_NAMESPACE="$(oci os ns get --query 'data' --raw-output)"

BUCKET_NAME="motando_moto"
DOCKER_IMG_VERSION="1.0"
DOCKER_IMG_NAME="motando-api-moto"
OCIR_IMG_NAME="$OCIR_ENDPOINT/$OBJSTR_NAMESPACE/$DOCKER_IMG_NAME"

function build_push() {       

   echo -e "[INFO] Building and Pushing the docker image to OCIR ...\n"

   docker build --no-cache \
        -t $DOCKER_IMG_NAME:$DOCKER_IMG_VERSION \
        -t $DOCKER_IMG_NAME:latest \
        container/

   docker tag $DOCKER_IMG_NAME:latest $OCIR_IMG_NAME:latest

   docker push $OCIR_IMG_NAME:latest

   echo -e "\n[INFO] Building and Pushing Successful!" 
   echo "[INFO] Exiting ..." 
}

function upload_data() {

   local src_dir="data/"

   oci os object bulk-upload \
      --no-follow-symlinks \
      --bucket-name "$BUCKET_NAME" \
      --src-dir "$src_dir" \
      --content-type "application/json" \
      --overwrite \
      --verify-checksum 
}

function pod_service() {

   kubectl create -f ./deployment.yaml

   if [ $? -ne 0 ]; then
      echo -e "\n[ERROR] POD Deployment error. Could not continue." 
      echo "[ERROR] Exiting ..."
      exit 1
   fi

   kubectl create -f ./service.yaml

   if [ $? -ne 0 ]; then
      echo -e "\n[ERROR] SERVICE Deployment error. Could not continue." 
      echo "[ERROR] Exiting ..."
      exit 1
   fi
}

function deploy() {

     echo -e "[INFO] Starting deploy API - MOTO ...\n"

     echo "[INFO] Uploading data to Object Storage (Bucket: $BUCKET_NAME) ..."
     upload_data

     echo -e "\n[INFO] Deployment POD and SERVICE ...\n"
     pod_service         
}

case $1 in 
     -bp|--bp|--build-push)
           build_push
           ;;   
      -fp|--fp|--full-deploy)
           build_push
           deploy
           ;;
      *)
           deploy
           ;;
esac

exit 0