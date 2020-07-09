FROM frolvlad/alpine-glibc

RUN apk update \                                                                                                                                                                                                                        
    &&   apk add ca-certificates wget \                                                                                                                                                                                                      
    &&   update-ca-certificates \
    && apk add --no-cache --upgrade bash

ARG POWERGATE_CLI_VERSION="v0.0.1-beta.13"

WORKDIR /opt/powcli

RUN wget -O powcli.tar.gz https://github.com/textileio/powergate/releases/download/${POWERGATE_CLI_VERSION}/pow_${POWERGATE_CLI_VERSION}_linux-amd64.tar.gz \
    && tar -xf powcli.tar.gz && ./install
