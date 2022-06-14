FROM ubuntu:20.04@sha256:c95a8e48bf88e9849f3e0f723d9f49fa12c5a00cfc6e60d2bc99d87555295e4c

ENV LC_ALL=C.UTF-8 LANG=C.UTF-8
ENV DEBIAN_FRONTEND=noninteractive

RUN dpkg --add-architecture i386 && \
    apt-get update -q && \
    apt-get install -qy \
        wget \
        gnupg2 \
        dirmngr \
        python3-software-properties \
        software-properties-common

RUN apt-get update -q && \
        apt-get install -qy \
        git \
        p7zip-full\
        make \
        mingw-w64 \
        mingw-w64-tools \
        win-iconv-mingw-w64-dev \
        autotools-dev \
        autoconf \
        autopoint \
        libtool \
        gettext

RUN wget -nc https://dl.winehq.org/wine-builds/Release.key && \
        echo "c51bcb8cc4a12abfbd7c7660eaf90f49674d15e222c262f27e6c96429111b822 Release.key" | sha256sum -c - && \
        apt-key add Release.key && \
        rm Release.key && \
    wget -nc https://dl.winehq.org/wine-builds/winehq.key && \
        echo "78b185fabdb323971d13bd329fefc8038e08559aa51c4996de18db0639a51df6 winehq.key" | sha256sum -c - && \
        apt-key add winehq.key && \
        rm winehq.key && \
    apt-add-repository https://dl.winehq.org/wine-builds/ubuntu/ && \
    apt-get update -q && \
    apt-get install -qy \
<<<<<<< HEAD
        wine-stable-amd64:amd64=7.0.0.0~focal-1 \
        wine-stable-i386:i386=7.0.0.0~focal-1 \
        wine-stable:amd64=7.0.0.0~focal-1 \
        winehq-stable:amd64=7.0.0.0~focal-1 \
        && \
    rm -rf /var/lib/apt/lists/* && \
=======
        wine-stable-amd64:amd64 \
        wine-stable-i386:i386 \
        wine-stable:amd64 \
        winehq-stable:amd64

RUN rm -rf /var/lib/apt/lists/* && \
>>>>>>> develop
    apt-get autoremove -y && \
    apt-get clean

# create new user to avoid using root; but with sudo access and no password for convenience.
ENV USER="user"
ENV HOME_DIR="/home/${USER}"
ENV WORK_DIR="${HOME_DIR}/wspace" \
    PATH="${HOME_DIR}/.local/bin:${PATH}"
RUN useradd --create-home --shell /bin/bash ${USER}
RUN usermod -append --groups sudo ${USER}
RUN echo "%sudo ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
WORKDIR ${WORK_DIR}
RUN chown --recursive ${USER} ${WORK_DIR}
RUN chown ${USER} /opt
USER ${USER}

RUN mkdir --parents "/opt/wine64/drive_c/electrum"
