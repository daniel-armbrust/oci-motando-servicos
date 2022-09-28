#!/bin/bash
#
# deploy.sh
#

current_dir="$(pwd)"

deployment_dir[0]="ingress-controller/"
deployment_dir[1]="frontend/"
deployment_dir[2]="api-estado-cidade/"
deployment_dir[3]="api-moto/"
deployment_dir[4]="api-usuario/"
deployment_dir[5]="api-anuncio/"
deployment_dir[6]="api-auth/"
deployment_dir[7]="api-gateway/20220304/"

case $1 in 
   -fp|--fp|--full-deploy)
      deploy_cmd="./deploy.sh -fp"
      ;;
   *)
      deploy_cmd="./deploy.sh"
      ;;
esac

i=0
while [ $i -lt ${#deployment_dir[*]} ]; do   
   cd "${deployment_dir[$i]}" && $deploy_cmd
   cd "$current_dir"
   let i+=1
done

exit 0