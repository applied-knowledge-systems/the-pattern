VERSION 0.7
PROJECT applied-knowledge-systems/the-pattern
FROM ubuntu:20.04
ARG TARGETARCH
ARG TARGETOS
ARG TARGETPLATFORM
ARG --global tag=$TARGETOS-$TARGETARCH
ARG --global TARGETARCH
IF [ "$TARGETARCH" = amd64 ]
    ARG --global ARCH=x86_64
ELSE
    ARG --global ARCH=$TARGETARCH
END

some-pipeline:
  PIPELINE --push
  TRIGGER push main
  TRIGGER pr main
  BUILD +redismod

all:
    BUILD \
        --platform=linux/amd64 \
        --platform=linux/aarch64 \
        # --platform=linux/arm/v7 \
        # --platform=linux/arm/v6 \


my-build:
  RUN echo Hello world
          
fetch-code:
    ENV DEBIAN_FRONTEND noninteractive
    ENV DEBCONF_NONINTERACTIVE_SEEN true
    RUN apt-get update && apt-get install -yqq --no-install-recommends build-essential libgomp1 git ca-certificates
    RUN update-ca-certificates
    RUN git clone --recurse-submodules https://github.com/applied-knowledge-systems/the-pattern.git the-pattern.git
    SAVE ARTIFACT the-pattern.git AS LOCAL the-pattern.git

build:
    FROM +fetch-code
    WORKDIR /the-pattern
    RUN false

redismod:
    FROM DOCKERFILE -f Dockerfile.latest .
    WORKDIR /code 
    COPY +fetch-code/the-pattern.git/the-pattern-platform/conf/redis_with_mods.conf /etc/redis/redis.conf
    # COPY ./the-pattern-platform/conf/redis_with_mods.conf /etc/redis/redis.conf
    COPY ./the-pattern-platform/conf/redis.service /etc/systemd/system/redis.service 
    SAVE IMAGE --push ghcr.io/applied-knowledge-systems/redismod:latest
    
