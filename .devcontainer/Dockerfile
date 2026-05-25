FROM maven:3.9.6-eclipse-temurin-17

ARG NODE_VERSION=18.19.1

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl git ca-certificates xz-utils \
    && curl -fsSL "https://nodejs.org/dist/v${NODE_VERSION}/node-v${NODE_VERSION}-linux-x64.tar.xz" -o /tmp/node.tar.xz \
    && mkdir -p /usr/local/lib/nodejs \
    && tar -xJf /tmp/node.tar.xz -C /usr/local/lib/nodejs \
    && ln -s /usr/local/lib/nodejs/node-v${NODE_VERSION}-linux-x64/bin/node /usr/local/bin/node \
    && ln -s /usr/local/lib/nodejs/node-v${NODE_VERSION}-linux-x64/bin/npm /usr/local/bin/npm \
    && ln -s /usr/local/lib/nodejs/node-v${NODE_VERSION}-linux-x64/bin/npx /usr/local/bin/npx \
    && rm -rf /var/lib/apt/lists/* /tmp/node.tar.xz

WORKDIR /workspace
