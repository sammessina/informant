Informant
=========
An information board designed to be easy to set up and use.

## Design

### Goals:
* Easy to set up
* Feature-rich

### Raspberry Pi Setup
1. Install [Raspbian](http://www.raspberrypi.org/downloads)
  * [2012-09-18-wheezy-raspbian](http://ftp.gnome.org/mirror/raspberrypi/images/raspbian/2012-09-18-wheezy-raspbian/2012-09-18-wheezy-raspbian.zip) seems to be more stable (2013+ drops network connection)
2. Config Raspbian
  * config.txt options
    * disable_overscan=1
    * hdmi_force_hotplug=1 (if VGA)
    * config_hdmi_boost=4 (if VGA)
    * framebuffer_depth=32
    * framebuffer_ignore_alpha=1
  * Inside of raspi-config:
    * Set timezone
    * Boot to desktop
    * Expand root fs
    * Finish
  * Config wifi if needed
  * Install PyBluez to enable bluetooth device detection
    * sudo apt-get install bluez python-bluez
  * (Future/Todo) For graphic acceleration, the Python Imaging Library must be installed
    * Add to config.txt: gpu_mem=128
    * sudo apt-get install python-imaging
3. If using 2012-09-18-wheezy-raspbian, do: sudo apt-get update --fix-missing
4. sudo apt-get install git
5. git clone https://github.com/youresam/informant.git
6. cd informant && chmod +x run_ci.sh && sudo ./run_ci.sh install

### Panes:
* Assignments
* Todo
* Clock
* Classes
* Time until wake
* Weather?
* Unread Email?

### Management:
* Data synced from server on internet - accessable anywhere
* Events can be sent from email?

### Hardware requirements:
* A large screen
* Hardware capable of running an operating system