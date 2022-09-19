#!/bin/bash
#
# ingress-controller/deploy.sh
#

function get_lb_ocid() {

   local lb_ocid=""

   lb_ocid="$(oci search resource structured-search \
      --query-text "query loadbalancer resources 
         where (freeformTags.key = 'motando' && freeformTags.value = 'ingress-nginx-controller' && lifeCycleState = 'ACTIVE')" \
      --query 'data.items[0].identifier' --raw-output)"
   
   echo -n "$lb_ocid"  
}

function get_lb_ip() {

   local lb_ocid="$1"

   local ip="$(oci lb load-balancer get --load-balancer-id "$lb_ocid" \
      --query "data.\"ip-addresses\"" | grep "ip-address" | awk '{print $2}' | tr -d '",')"

   echo -n "$ip"
}

function update_dns() {

    local lb_ip="$1"  

    local compartment_dns="cmp-dns"
    local view_id=""

    local dns_zone="ocibook.local"
    local dns_record="api.ocibook.local"
    local ttl=30

    compartment_dns="$(oci search resource structured-search \
        --query-text "query compartment resources where displayName = \"$compartment_dns\"" \
        --query 'data.items[0].identifier' --raw-output)"
    
    view_id="$(oci dns zone list --compartment-id "$compartment_dns" --scope PRIVATE \
        --query "data[0].\"view-id\"" --raw-output)"

    if [ ! -z "$view_id" ]; then

        oci dns record domain update \
           --zone-name-or-id "$dns_zone" \
           --domain "$dns_record" \
           --compartment-id "$compartment_dns" \
           --view-id "$view_id" \
           --scope "PRIVATE" \
           --force \
           --items "[{\"domain\": \"$dns_record\", \"rdata\": \"$lb_ip\", \"rtype\": \"A\", \"ttl\": $ttl}]" 1>/dev/null

    else
       echo -e "\n[ERROR] The private dns \"view-id\" could not be found."
       echo "[ERROR] Deployment error. Could not continue." 
       echo "[ERROR] Exiting ..."
       exit 1
    fi
}

function ingress_controller() {

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
}

function deploy() {
    
    local lb_ocid=""
    local lb_ip=""  

    local max_tries=20
    local count=1
    local sleep_seconds="10s"      

    echo -e "[INFO] Starting deploy INGRESS-CONTROLLER ...\n"
    
    ingress_controller  

    echo -e "\n[INFO] Waiting for Load Balancer to become available ..."   

    while [ $count -le $max_tries ]; do
       echo -ne "\t[wait $sleep_seconds ($count)] "

       lb_ocid="$(get_lb_ocid)"

       if [ ! -z "$lb_ocid" ]; then
          echo -e "\n\n[INFO] Getting Load Balancer PRIVATE IP ..."
          lb_ip="$(get_lb_ip $lb_ocid)"

          echo "[INFO] Updating the internal DNS ..."
          update_dns "$lb_ip"

          break
       else
          let count+=1
          sleep "$sleep_seconds" 
       fi

    done   

    if [ -z "$lb_ocid" ]; then
       echo -e "\n[ERROR] Deployment error. Could not continue." 
       echo "[ERROR] Exiting ..."
       exit 1
    else
       echo -e "\n[INFO] Deployment Successful!" 
       echo "[INFO] Exiting ..." 
    fi
}

deploy

exit 0