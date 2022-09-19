#!/bin/bash
#
# usuario/deploy.sh
#

OCIR_ENDPOINT="gru.ocir.io"
OBJSTR_NAMESPACE="$(oci os ns get --query 'data' --raw-output)"

BUCKET_NAME="motando_usuario"
DOCKER_IMG_VERSION="1.0"
DOCKER_IMG_NAME="motando-api-usuario"
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

     echo -e "[INFO] Starting deploy API - USUARIO ...\n"
     
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