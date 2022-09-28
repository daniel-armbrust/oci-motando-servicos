#!/bin/bash
#
# undeploy.sh
#

current_dir="$(pwd)"

undeployment_dir[0]="api-gateway/20220304/"
undeployment_dir[1]="frontend/"
undeployment_dir[2]="api-estado-cidade/"
undeployment_dir[3]="api-moto/"
undeployment_dir[4]="api-usuario/"
undeployment_dir[5]="api-anuncio/"
undeployment_dir[6]="api-auth/"
undeployment_dir[7]="ingress-controller/"

i=0
while [ $i -lt ${#undeployment_dir[*]} ]; do
   cd "${undeployment_dir[$i]}" && ./undeploy.sh 
   cd "$current_dir"
   let i+=1
done

exit 0