#!/bin/bash

# This script acts like a continuous integration client for informant board.
# The latest code is pulled from
# Directions:
#   Run this script normally and the latest code will be synced in ./informant/
#   To set as startup on raspberry pi: run_ci --install

# Spec: Running this file normally copies its directory to tmp and runs from there by
#       using the args: run <origindir>

# To reset during testing: git fetch --all && git reset --hard origin/master && chmod +x run_ci.sh

# local vars
localdir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" #http://stackoverflow.com/a/246128
synceddir="$2"
this_script_hash=($(md5sum ${localdir}/run_ci.sh))

# Set as startup program on raspberry pi
function install {
    #add line (if not exists) to /etc/xdg/lxsession/LXDE/autostart
    # @/home/pi/board/informant/run_ci.sh
    exit #todo
}

# Remove as startup program on raspberry pi
function uninstall {
    exit #todo
}

function start_informant {
    echo "starting informant"
    cd ${localdir}/src && python informant.py &
}

function stop_informant {
    echo "stopping informant"
    pkill -f informant.py
}

function query_git {
    echo "querying remote repo"
    cd ${synceddir}
    [ "`git log --pretty=%H ...refs/heads/master^ | head -n 1`" = "`git ls-remote origin -h refs/heads/master |cut -f1`" ] && changed=0 || changed=1 #http://stackoverflow.com/a/16920556
    echo "git changed=${changed}"
    if [ ${changed} -eq 1 ]; then
        update
    fi
}

function update {
    echo "updating informant"
    stop_informant
    #git pull
    cd ${synceddir}
    git fetch --all
    git reset --hard origin/master
    chmod +x ${synceddir}/run_ci.sh
    new_script_hash=($(md5sum ${synceddir}/run_ci.sh))
    echo "new hash = $new_script_hash, old hash = $this_script_hash"
    if [ "$new_script_hash" != "$this_script_hash" ]; then
        echo "CI script updated, restarting..."
        ${synceddir}/run_ci.sh &
        exit 0
    fi
    start_informant
}

function run {
    echo "synceddir=$synceddir"
    stop_informant
    if [ $(pidof -x run_ci.sh | wc -w) -gt 2 ]; then
        echo "killing other run_ci process"
        kill `pidof -x -o $$ run_ci.sh`
    fi
    start_informant

    while true; do
        query_git
        sleep 30
    done
}

if [ "$1" == "run" ]; then
    run
    exit 0
fi

# copy over to tmp to run
# this is because run_ci.sh was being zeroed
tmpdir=`mktemp -d`
cp -rf ${localdir} ${tmpdir}
${tmpdir}/informant/run_ci.sh run ${localdir}