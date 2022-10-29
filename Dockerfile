FROM alpine:3.16
LABEL maintainer="Thomas GUIRRIEC <thomas@guirriec.fr>"
ENV SPEEDTEST_HOST=""
ENV SPEEDTEST_EXPORTER_PORT=8123
ENV SPEEDTEST_EXPORTER_LOGLEVEL='INFO'
ENV SPEEDTEST_EXPORTER_NAME='speedtest-exporter'
ENV SCRIPT='speedtest_exporter.py'
ENV USERNAME="exporter"
ENV UID="1000"
ENV GID="1000"
COPY apk_packages /
COPY pip_packages /
ENV VIRTUAL_ENV="/dockerhub-limit-exporter"
ADD https://install.speedtest.net/app/cli/ookla-speedtest-1.2.0-linux-x86_64.tgz /tmp/speedtest.tar.gz
ENV VIRTUAL_ENV="/speedtest-exporter"
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN xargs -a /apk_packages apk add --no-cache --update \
    && python3 -m venv "${VIRTUAL_ENV}" \
    && pip install --no-cache-dir --no-dependencies --no-binary :all: -r pip_packages \
    && pip uninstall -y setuptools pip \
    && tar xzvf /tmp/speedtest.tar.gz -C /usr/local/bin \
    && useradd -l -u "${UID}" -U -s /bin/sh -m "${USERNAME}" \
    && rm -rf \
        /root/.cache \
        /tmp/* \
        /var/cache/* \
    && chown ${USERNAME}:${USERNAME} /usr/local/bin/speedtest \
    && chmod +x /usr/local/bin/speedtest
COPY --chown=${USERNAME}:${USERNAME} --chmod=500 ${SCRIPT} ${VIRTUAL_ENV}
COPY --chown=${USERNAME}:${USERNAME} --chmod=500 entrypoint.sh /
USER ${USERNAME}
WORKDIR ${VIRTUAL_ENV}
EXPOSE ${SPEEDTEST_EXPORTER_PORT}
HEALTHCHECK CMD nc -vz localhost ${SPEEDTEST_EXPORTER_PORT} || exit 1
ENTRYPOINT ["/entrypoint.sh"]
