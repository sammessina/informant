#! /bin/bash
# /etc/init.d/config_pi

### BEGIN INIT INFO
# Provides:          config_pi
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Configures system settings of the raspberry pi
# Description:       Configures system settings of the raspberry pi
### END INIT INFO

# This script configures system settings of the raspberry pi
# To run:
#   wget https://raw.githubusercontent.com/youresam/informant/master/config_pi.sh
#   chmod +x config_pi.sh
#   ./config_pi.sh
# Settings configured:
#   * Run initial raspi-config
#   * Configure config.txt
#   * Wifi

# local vars
localdir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" #http://stackoverflow.com/a/246128
NEED_TO_REBOOT=0

if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

# Set as startup program on raspberry pi
function install {
    echo "Installing config service"
    ln -s ${localdir}/config_pi.sh /etc/init.d/config_pi
    update-rc.d config_pi defaults
    exit 0
}

function uninstall {
    update-rc.d config_pi remove
    unlink /etc/init.d/config_pi
}

# Taken from raspi-config script
set_config_var() {
  lua - "$1" "$2" "$3" <<EOF > "$3.bak"
local key=assert(arg[1])
local value=assert(arg[2])
local fn=assert(arg[3])
local file=assert(io.open(fn))
local made_change=false
for line in file:lines() do
  if line:match("^#?%s*"..key.."=.*$") then
    line=key.."="..value
    made_change=true
  end
  print(line)
end

if not made_change then
  print(key.."="..value)
end
EOF
mv "$3.bak" "$3"
}

# Taken from raspi-config script
get_config_var() {
    if [ -f "$2" ]; then
  lua - "$1" "$2" <<EOF
local key=assert(arg[1])
local fn=assert(arg[2])
local file=assert(io.open(fn))
for line in file:lines() do
  local val = line:match("^#?%s*"..key.."=(.*)$")
  if (val ~= nil) then
    print(val)
    break
  end
end
EOF
fi
}

function run_raspi-config {
    # Set timezone
    currzone=$(echo /etc/timezone)
    v=$(get_config_var timezone /boot/informant.ini)
    if [ -n "${v}" ] && [ "${v}" != "${currzone}" ]; then
        echo "setting timezone to ${v}"
        echo "${v}" > /etc/timezone
        dpkg-reconfigure -f noninteractive tzdata
    fi

    # Boot to desktop
    update-rc.d lightdm enable 2
    sed /etc/lightdm/lightdm.conf -i -e "s/^#autologin-user=.*/autologin-user=pi/"
    rm -f /etc/profile.d/raspi-config.sh
    sed -i /etc/inittab \
      -e "s/^#\(.*\)#\s*RPICFG_TO_ENABLE\s*/\1/" \
      -e "/#\s*RPICFG_TO_DISABLE/d"

}

function enforce_setting {
    v=$(get_config_var $1 /boot/config.txt)
    if [ -z "${v}" ] || [ "${v}" != "$2" ]; then
        echo "setting $1=$2 (was ${v})"
        set_config_var $1 $2 /boot/config.txt
    fi
}

function check_config {
    enforce_setting framebuffer_depth 32
    enforce_setting framebuffer_ignore_alpha 1
    enforce_setting disable_overscan 1
}

function try_config_wifi {
    config_wifi=$(get_config_var config_wifi /boot/informant.ini)
    wifi_ssid=$(get_config_var wifi_ssid /boot/informant.ini)
    wifi_password=$(get_config_var wifi_password /boot/informant.ini)
    echo "config_wifi=${config_wifi}, wifi_ssid=${wifi_ssid}"
    if [ "${config_wifi}" == "Yes" ] && [ "${wifi_ssid}" ]; then
        # This file: /etc/network/interfaces
        # Needs to contain lines:
        #   wpa-ssid "ssid"
        #   wpa-psk "password"
        ssid_ok=$(grep -q "wpa-ssid \"${wifi_ssid}\"" "/etc/network/interfaces")
        password_ok=$(grep -q "wpa-psk \"${wifi_password}\"" "/etc/network/interfaces")
        if [ ${ssid_ok} ] && [ ${password_ok} ]; then
            echo "Wifi config ok"
        else
            echo "Configuring wifi"
            printf "auto lo\niface lo inet loopback\niface eth0 inet dhcp\nallow-hotplug wlan0\nauto wlan0\niface wlan0 inet dhcp\nwpa-ssid \"${wifi_ssid}\"\nwpa-psk \"${wifi_password}\"" >  /etc/network/interfaces
            NEED_TO_REBOOT=1
        fi
    else
        echo "Skipping wifi config"
    fi
}

function main {
    echo "config_pi running"
    config_settings=$(get_config_var config_wifi /boot/informant.ini)
    if [ "${config_settings}" == "Yes" ]; then
        run_raspi-config
        check_config
    fi
    try_config_wifi
    #if [ ${NEED_TO_REBOOT} == 1 ]; then
    #    reboot
    #fi
}

if [ "$1" == "install" ]; then
    install
    exit 0
fi

if [ "$1" == "uninstall" ]; then
    uninstall
    exit 0
fi

if [ "$1" == "stop" ]; then
    # Not a real service, so ignore this
    echo "Ignoring command"
    exit 0
fi

main