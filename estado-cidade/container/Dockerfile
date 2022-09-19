#
# Dockerfile - estado_cidade
#
FROM container-registry.oracle.com/os/oraclelinux:8-slim

LABEL maintainer="Daniel Armbrust <darmbrust@gmail.com>"

ENV PYTHONUNBUFFERED=1

WORKDIR /opt/estado_cidade

COPY requirements.txt ./
COPY docker-entrypoint.sh ./

RUN microdnf update -y && \
    microdnf install -y python3.8 && \
    python -m ensurepip && \
    ln -sf /usr/local/bin/pip3 /usr/local/bin/pip && \
    pip install --no-cache-dir --upgrade pip setuptools && \
    pip install --no-cache-dir -r requirements.txt && \
    microdnf clean all && rm -rf /var/cache/yum

RUN adduser -l -d /opt/estado_cidade api

COPY --chown=api:api ./app/ /opt/estado_cidade/

USER api

EXPOSE 5000

ENTRYPOINT ["./docker-entrypoint.sh"]