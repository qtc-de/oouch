#!/bin/bash

set -ex

###########################
#     install depends     #
###########################
apt -y install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg2 \
    software-properties-common

###########################
#     add docker repo     #
###########################
curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add -

add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/debian \
   $(lsb_release -cs) \
   stable"

###########################
#     install docker      #
###########################
apt update
apt -y install docker-ce docker-ce-cli containerd.io
