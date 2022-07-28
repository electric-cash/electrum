FROM ubuntu:20.04

ENV LC_ALL=C.UTF-8 LANG=C.UTF-8

ENV LC_ALL=C.UTF-8 LANG=C.UTF-8
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update -qy
RUN TZ=Europe/Warsaw apt-get -y install tzdata

RUN apt-get install -qy \
        git \
        wget \
        make \
        autotools-dev \
        autoconf \
        libtool \
        xz-utils \
        libssl-dev \
        libssl1.1 \
        openssl \
        zlib1g-dev \
        libffi-dev \
        libncurses5-dev \
        libsqlite3-dev \
        libusb-1.0-0-dev \
        libudev-dev \
        gettext \
        libzbar0 \
        libdbus-1-3 \
        libxkbcommon-x11-0 \
        libc6-dev \
        && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get autoremove -y && \
    apt-get clean
