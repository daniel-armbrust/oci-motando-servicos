#
# Dockerfile - NGINX
#
FROM container-registry.oracle.com/os/oraclelinux:8-slim

LABEL maintainer="Daniel Armbrust <darmbrust@gmail.com>"

RUN microdnf update -y && \
    microdnf install -y nginx && \
    microdnf clean all && \
    mkdir -p /srv/motando-ocibook-com-br/ && \
    rm -f /etc/nginx/nginx.conf && \
    rm -rf /usr/share/nginx/ && \
    rm -rf /var/cache/yum
    
COPY nginx.conf /etc/nginx/nginx.conf

# https://github.com/nginxinc/docker-nginx/blob/master/mainline/alpine/Dockerfile
RUN  mkdir /docker-entrypoint.d
COPY docker-entrypoint.sh /
COPY 10-listen-on-ipv6-by-default.sh /docker-entrypoint.d
COPY 20-envsubst-on-templates.sh /docker-entrypoint.d
COPY 30-tune-worker-processes.sh /docker-entrypoint.d
ENTRYPOINT ["/docker-entrypoint.sh"]

EXPOSE 80

STOPSIGNAL SIGQUIT

CMD ["nginx", "-g", "daemon off;"]