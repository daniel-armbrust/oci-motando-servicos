#
# Dockerfile - Frontend
#
FROM container-registry.oracle.com/os/oraclelinux:8-slim

LABEL maintainer="Daniel Armbrust <darmbrust@gmail.com>"

ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=main.py
ENV FLASK_DEBUG=0
ENV FLASK_ENV=production

WORKDIR /opt/frontend

COPY requirements.txt ./
COPY docker-entrypoint.sh ./

RUN microdnf update -y && \
    microdnf install -y python3.8 && \
    python -m ensurepip && \
    ln -sf /usr/local/bin/pip3 /usr/local/bin/pip && \
    pip install --no-cache-dir --upgrade pip setuptools && \
    pip install --no-cache-dir -r requirements.txt && \
    microdnf clean all && rm -rf /var/cache/yum

RUN adduser -l -d /opt/frontend frontend

COPY --chown=frontend:frontend ./app/ /opt/frontend/

# HTML Minify
#RUN ls -1R /opt/frontend/templates/*.html | while read html_file ; do \
RUN shopt -s globstar dotglob ; ls -1d ./**/*.html | while read html_file ; do \       
       sed -e "s/^[ \t]*//g" -e "/^$/d" -i "$html_file"; \
       sed ':a;N;$!ba;s/>\s*</></g' -i "$html_file"; \
       sed '/^[[:space:]]*$/d' -i "$html_file"; \
    done

USER frontend

EXPOSE 5000

ENTRYPOINT ["./docker-entrypoint.sh"]