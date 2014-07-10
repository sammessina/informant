#!/bin/bash

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
    if [ -f "2" ]; then
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

function check_config {
    v=$(get_config_var framebuffer_depth /boot/config.txt)
    if [ -z "${v}" ] || [ "${v}" != "32" ]; then
        echo "setting framebuffer_depth=32 (was ${v})"
        set_config_var framebuffer_depth 32 /boot/config.txt
    fi

    v=$(get_config_var framebuffer_ignore_alpha /boot/config.txt)
    if [ -z "${v}" ] || [ "${v}" != "1" ]; then
        echo "setting framebuffer_ignore_alpha=1"
        set_config_var framebuffer_ignore_alpha 1 /boot/config.txt
    fi

    v=$(get_config_var disable_overscan /boot/config.txt)
    if [ -z "${v}" ] || [ "${v}" != "1" ]; then
        echo "setting disable_overscan=1"
        set_config_var disable_overscan 1 /boot/config.txt
    fi
}

function config_wifi {
    config_wifi=$(get_config_var config_wifi /boot/informant.ini)
    wifi_ssid=$(get_config_var wifi_ssid /boot/informant.ini)
    wifi_password=$(get_config_var wifi_password /boot/informant.ini)
    if [ "${config_wifi}" == "Yes" ]; then
        # This file: /etc/network/interfaces

        # Check for "auto wlan0"
        if grep -q "auto wlan0" "/etc/network/interfaces"; then
            echo "wlan0 set to automatic"
        else
            echo "setting wlan0 to auto"
            printf "\nauto wlan0" >> /etc/network/interfaces
            NEED_TO_REBOOT=1
        fi

        # Disable auto config file
        if grep -q "^wpa-roam" "/etc/network/interfaces"; then
            echo "Deleting wpa-roam setting"
            sed -i '/^wpa-roam /d' /etc/network/interfaces
            NEED_TO_REBOOT=1
        fi

        if grep -q "iface wlan0 inet manual" "/etc/network/interfaces"; then
            echo "Setting wlan0 to DHCP"
            sed -i -e "s/^iface wlan0 inet manual/iface wlan0 inet dhcp/" /etc/network/interfaces
            NEED_TO_REBOOT=1
        fi


        # Needs to contain lines:
        #   wpa-ssid "ssid"
        #   wpa-psk "password"

        if grep -q "wpa-ssid" "/etc/network/interfaces"; then
            # File has an entry already
            # Is it the correct one?
            if grep -q "wpa-ssid \"${wifi_ssid}\"" "/etc/network/interfaces"; then
                # Yes it is
                echo "Wifi already set up correctly"
            else
                # Nope, fix it
                echo "Configuring wifi"
                sed -i '/wpa-ssid /d' /etc/network/interfaces
                sed -i '/wpa-psk /d' /etc/network/interfaces
                printf "\nwpa-ssid \"${wifi_ssid}\"\nwpa-psk \"${wifi_password}\"" >> /etc/network/interfaces
                NEED_TO_REBOOT=1
            fi
        else
            # file doesnt contain any ssid entry
            # Add entry
            echo "Adding wifi config"
            printf "\nwpa-ssid \"${wifi_ssid}\"\nwpa-psk \"${wifi_password}\"" >> /etc/network/interfaces
            NEED_TO_REBOOT=1
        fi
    fi
}

function main {
    run_raspi-config
    check_config
    config_wifi
    if [ ${NEED_TO_REBOOT} == 1 ]; then
        reboot
    fi
}

if [ "$1" == "install" ]; then
    install
    exit 0
fi

if [ "$1" == "uninstall" ]; then
    uninstall
    exit 0
fi

main