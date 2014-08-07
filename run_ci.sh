#!/bin/bash

# This script acts like a continuous integration client for informant board.
# The latest code is pulled from
# Directions:
#   Run this script normally and the latest code will be synced in ./informant/
#   To set as startup on raspberry pi: run_ci --install

# Spec: Running this file normally copies its directory to tmp and runs from there by
#       using the args: run <origindir>

#fixme: this file keeps getting erased on shutdown and I don't know why. workaround is to run within cmd window
# A workaround: launch the file from the terminal instead of directly
# To reset during testing: git fetch --all && git reset --hard origin/master && chmod u+x *.sh

# local vars
localdir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" #http://stackoverflow.com/a/246128
changed=0

# Set as startup program on raspberry pi
function install {
    #add line (if not exists) to /etc/xdg/lxsession/LXDE/autostart
    if grep -q "run_ci" "/etc/xdg/lxsession/LXDE/autostart"; then
        echo "Already installed"
    else
        echo "Installing to /etc/xdg/lxsession/LXDE/autostart"
        printf "\nlxterminal -e \"${localdir}/run_ci.sh\"" >> /etc/xdg/lxsession/LXDE/autostart
    fi
    exit 0
}

# Remove as startup program on raspberry pi
function uninstall {
    echo "Uninstalling from /etc/xdg/lxsession/LXDE/autostart"
    sed -i '/run_ci\.sh/d' /etc/xdg/lxsession/LXDE/autostart
    exit 0
}

function start_informant {
    stop_informant
    echo "starting informant"
    cd ${localdir}/src && python main.py &
}

function stop_informant {
    echo "stopping informant"
    pkill -f main.py
}

function query_git {
    # echo "querying remote repo"
    cd ${localdir}
    changed=0
    log="`git ls-remote origin -h refs/heads/master | cut -f1`"
    if [ ${#log} -eq 40 ]; then
        [ "$log" = "`git log --pretty=%H ...refs/heads/master^ | head -n 1`" ] && changed=0 || changed=1 #http://stackoverflow.com/a/16920556
        # echo "git changed=${changed}"
    fi
    if [ ${changed} -eq 1 ]; then
        update
        #run_ci.sh
        #exit 0
    else
        # check if it's crashed
        ps aux | grep -v grep | grep "python main.py" > /dev/null || start_informant
    fi
}

function update {
    echo "updating informant"
    cd ${localdir}
    git fetch --all && git reset --hard origin/master && chmod u+x *.sh
    start_informant
}

function main {
    #query_git
    start_informant
    while true; do
        query_git
        sleep 30
    done
}

if [ "$1" == "install" ]; then
    install
fi

if [ "$1" == "uninstall" ]; then
    uninstall
fi

main