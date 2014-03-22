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
    cd ${localdir}
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
    cd ${localdir}
    git fetch --all
    git reset --hard origin/master
    chmod +x ${localdir}/run_ci.sh
    #todo ensure pull works no matter what
    new_script_mtime=`stat -c%Y ${localdir}/run_ci.sh`
    echo "$new_script_mtime = $new_script_mtime, this_script_mtime = $this_script_mtime "
    if [ "$new_script_mtime" -ne "$this_script_mtime" ]; then
        echo "CI script updated, restarting..."
        ${localdir}/run_ci.sh &
        exit 0
    fi
    start_informant
}

#pkill -f run_ci.sh
if [ `pidof -x -o $$ run_ci.sh` -gt 0 ]; then
    echo "killing other run_ci process"
    kill `pidof -x -o $$ run_ci.sh`
fi
stop_informant
start_informant

while true; do
    query_git
    sleep 10
done