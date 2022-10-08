FROM alpine:3.16
LABEL maintainer="Thomas GUIRRIEC <thomas@guirriec.fr>"
ENV SPEEDTEST_HOST=""
ENV SPEEDTEST_EXPORTER_PORT=8123
ENV SPEEDTEST_EXPORTER_LOGLEVEL='INFO'
ENV SPEEDTEST_EXPORTER_NAME='speedtest-exporter'
COPY --chmod=755 requirements.txt /
COPY --chmod=755 entrypoint.sh /
ADD --chmod=755 https://install.speedtest.net/app/cli/ookla-speedtest-1.2.0-linux-x86_64.tgz /usr/local/bin
ENV VIRTUAL_ENV="/speedtest-exporter"
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN apk add --no-cache --update \
         python3 \
    && python3 -m venv ${VIRTUAL_ENV} \
    && pip install --no-cache-dir --no-dependencies --no-binary :all: -r requirements.txt \
    && pip uninstall -y setuptools pip \
    && rm -rf \
        /root/.cache \
        /tmp/* \
        /var/cache/*
COPY speedtest_exporter.py ${VIRTUAL_ENV}
WORKDIR ${VIRTUAL_ENV}
HEALTHCHECK CMD nc -vz localhost ${SPEEDTEST_EXPORTER_PORT} || exit 1
ENTRYPOINT ["/entrypoint.sh"]
