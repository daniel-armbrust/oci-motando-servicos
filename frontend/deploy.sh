#!/bin/bash
#
# frontend/deploy.sh
#

OCIR_ENDPOINT="gru.ocir.io"
OBJSTR_NAMESPACE="$(oci os ns get --query 'data' --raw-output)"

DOCKER_APP_IMG_VERSION="1.0"
DOCKER_APP_IMG_NAME="motando-frontend"
OCIR_APP_IMG_NAME="$OCIR_ENDPOINT/$OBJSTR_NAMESPACE/$DOCKER_APP_IMG_NAME"

DOCKER_NGINX_IMG_VERSION="1.0"
DOCKER_NGINX_IMG_NAME="motando-nginx"
OCIR_NGINX_IMG_NAME="$OCIR_ENDPOINT/$OBJSTR_NAMESPACE/$DOCKER_NGINX_IMG_NAME"

LB_BACKENDSET_NAME="bckset-1_albpub-motando_prd"
LB_NAME="albpub-motando_prd"
CLUSTERIP_SERVICE_PORT=30080

function build_push() {       

    echo -e "[INFO] Building and Pushing the docker image to OCIR ...\n"

    ## APP
    docker build --no-cache \
        -t $DOCKER_APP_IMG_NAME:$DOCKER_APP_IMG_VERSION \
        -t $DOCKER_APP_IMG_NAME:latest \
        container-app/
    
    docker tag $DOCKER_APP_IMG_NAME:latest $OCIR_APP_IMG_NAME:latest

    docker push $OCIR_APP_IMG_NAME:latest

    ## NGINX
    docker build --no-cache \
        -t $DOCKER_NGINX_IMG_NAME:$DOCKER_NGINX_IMG_VERSION \
        -t $DOCKER_NGINX_IMG_NAME:latest \
        container-nginx/
    
    docker tag $DOCKER_NGINX_IMG_NAME:latest $OCIR_NGINX_IMG_NAME:latest

    docker push $OCIR_NGINX_IMG_NAME:latest

    echo -e "\n[INFO] Building and Pushing Successful!" 
}

function get_lb_ocid() {

   local lb_ocid=""
   local json_backendset=""

   lb_ocid="$(oci search resource structured-search \
      --query-text "query loadbalancer resources 
         where (displayName = '$LB_NAME' && lifeCycleState = 'ACTIVE')" \
      --query 'data.items[0].identifier' --raw-output)"
   
   echo -n "$lb_ocid"  
}

function add_lb_backendset() {

   local lb_ocid="$1"

   local lb_backendset=""

   echo -e "[INFO] Adding Load Balancer ($LB_NAME) Backend Set ($LB_BACKENDSET_NAME) ..."
   
   lb_backendset="$(oci lb backend-set get \
      --load-balancer-id "$lb_ocid" \
      --backend-set-name "$LB_BACKENDSET_NAME" \
      --query 'data.backends' 2>/dev/null)"
   
   if [ ! -z "$lb_backendset" ]; then
      echo "[WARN] The \"$LB_BACKENDSET_NAME\" has some servers on it ..."
      echo "[WARN] Could not add more servers."
   else

      for node in $(kubectl get nodes -o wide | awk '{print $6}' | grep -v "INTERNAL-IP"); do 
         json_backendset="$(echo -n "$json_backendset" ; echo -n {\"ipAddress\": \"$node\", \"port\": $CLUSTERIP_SERVICE_PORT},)"
      done

      json_backendset=${json_backendset::-1}
      json_backendset="[$json_backendset]"

      oci lb backend-set update \
          --load-balancer-id "$lb_ocid" \
          --backend-set-name "$LB_BACKENDSET_NAME" \
          --policy "ROUND_ROBIN" \
          --health-checker-protocol "TCP" \
          --health-checker-port "$CLUSTERIP_SERVICE_PORT" \
          --backends "$json_backendset" \
          --wait-for-state SUCCEEDED \
          --force
   fi
}

function deploy() {

    local lb_ocid=""

    echo -e "[INFO] Starting deploy Motando FRONTEND ...\n"

    lb_ocid="$(get_lb_ocid)"

    if [ -z "$lb_ocid" ]; then
       echo -e "\n[ERROR] Deployment error. Could not continue." 
       echo "[ERROR] Exiting ..."
       exit 1
    fi

    add_lb_backendset "$lb_ocid"

    kubectl create -f ./deployment.yaml

    if [ $? -ne 0 ]; then
        echo -e "\n[ERROR] Deployment error. Could not continue." 
        echo "[ERROR] Exiting ..."
        exit 1
    fi

    kubectl create -f ./service.yaml

    if [ $? -ne 0 ]; then
        echo -e "\n[ERROR] Deployment error. Could not continue." 
        echo "[ERROR] Exiting ..."
        exit 1
    fi        

    echo -e "\n[INFO] Deployment Successful!" 
    echo "[INFO] Exiting ..."
}

case $1 in 
     -bp|--bp|--build-push)
           build_push
           ;;  

      # TODO: deploy only POD, deploy only SERVICE

      -fp|--fp|--full-deploy)
           build_push
           deploy
           ;;
      *)
           deploy
           ;;
esac

exit 0