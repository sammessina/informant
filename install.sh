#!/bin/bash

# This script is run independently from the rest. It is the bootstrap for configuring the system and installing
# informant.
# To run (first time setup):
#   > wget -O - https://raw.githubusercontent.com/youresam/informant/master/install.sh | sudo bash
# The following steps are run:
#   * Install needed packages
#   * Download repo from github
#   * chmod .sh files to allow execution
#   * install configurer
#   * install continuous integration runner
#   * run configurer

if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

function install_packages {
    apt-get update
    apt-get -y install git bluez python-bluez
}

function download_repo {
    su -c "git clone https://github.com/youresam/informant.git" pi
    chmod u+x informant/*.sh
}

function install_scripts {
    ./informant/config_pi.sh install
    ./informant/run_ci.sh install
}

function run_configurer {
    ./informant/config_pi.sh
}

function main {
    cd ~pi
    install_packages
    download_repo
    install_scripts
    run_configurer
}

main