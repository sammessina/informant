Informant
=========
An information board designed to be easy to set up and use.

### Automatic Raspberry Pi Setup
1. Install [Raspbian](http://www.raspberrypi.org/downloads)
2. Edit informant.ini and copy it to the SD card root (in Windows)
2. Log in
3. Run: wget -O - https://raw.githubusercontent.com/youresam/informant/master/install.sh | sudo bash
4. Run: sudo reboot


### Raspberry Pi Setup
1. Install [Raspbian](http://www.raspberrypi.org/downloads)
  * Ensure A/C plug used is rated for enough current, at least 1 amp.
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

### (todo) Management:
* Data synced from server on internet - accessable anywhere
* Events can be sent from email?
