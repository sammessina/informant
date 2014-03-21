#!/bin/bash

# This script acts like a continuous integration client for informant board.
# The latest code is pulled from
# Directions:
#   Run this script normally and the latest code will be synced in ./informant/
#   To set as startup on raspberry pi: run_ci --install

# local vars
localdir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" #http://stackoverflow.com/a/246128
this_script_mtime=`stat -c%Y run_ci.sh`

# Set as startup program on raspberry pi
function install {
    exit #todo
}

# Remove as startup program on raspberry pi
function uninstall {
    exit #todo
}

function start_informant {
    python ${localdir}/src/informant.py
}

function stop_informant {
    killall -w informant.py
}

function query_git {
    [ "`git log --pretty=%H ...refs/heads/master^ | head -n 1`" = "`git ls-remote origin -h refs/heads/master |cut -f1`" ] && changed=0 || changed=1 #http://stackoverflow.com/a/16920556
    if [ ${changed} -eq 1 ]
     then
        update
    fi
}

function update {
    git pull
    #todo ensure pull works no matter what
    new_script_mtime=`stat -c%Y run_ci.sh`
    if [ "$new_script_mtime" -ne "$this_script_mtime" ]
     then
        echo "CI script updated, restarting..."
        ${localdir}/run_ci.sh &
        exit 0
    fi
    stop_informant
    start_informant
}

start_informant

while true; do
    query_git
    sleep 300 #5 mins
done