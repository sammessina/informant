#!/bin/bash

# This script acts like a continuous integration client for informant board.
# The latest code is pulled from
# Directions:
#   Run this script normally and the latest code will be synced in ./informant/
#   To set as startup on raspberry pi: run_ci --install

# local vars
changed=0
localdir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" #http://stackoverflow.com/a/246128
this_script_mtime=`stat -c%Y run_ci.sh`
echo "script mtime="
echo ${this_script_mtime}
# Set as startup program on raspberry pi
function install {
    exit
}

# Remove as startup program on raspberry pi
function uninstall {
    exit
}

function start_informant {
    python ${localdir}/src/informant.py
}

function stop_informant {
    killall -w informant.py
}

function query_git {
    [ "`git log --pretty=%H ...refs/heads/master^ | head -n 1`" = "`git ls-remote origin -h refs/heads/master |cut -f1`" ] && changed=0 || changed=1 #http://stackoverflow.com/a/16920556
}

init_git

query_git

exit 0


start_informant

while true; do
    exit
done