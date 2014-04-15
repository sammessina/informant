Informant
=========
An information board designed to be easy to set up and use.

## Design

### Goals:
* Easy to set up
* Feature-rich

### Raspberry Pi Setup
1. Install [Raspbian](http://www.raspberrypi.org/downloads)
2. Config Raspbian
  * config.txt options
    * disable_overscan=1
    * hdmi_force_hotplug=1 (if VGA)
    * config_hdmi_boost=4 (if VGA)
    * framebuffer_depth=32
    * framebuffer_ignore_alpha=1
  * Boot to desktop
  * Wifi
3. git clone https://github.com/youresam/informant.git
4. cd informant && sudo ./run_ci.sh install

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

### Technologies:
* Output needs to be beautiful and responsive
* Possiblities:
  * Webpage:
    * Powered by PHP, output using elements or HTML5 canvas
    * Google Chrome has beautiful font rendering
    * Ajax for data sync, handled by Javascript
    * Might be hard to handle stuff that needs to be persistant, like an IMAP connection
    * Very big pro: easy to set up anywhere, assuming it's on an internet site
  * Executable:
    * Perhaps powered by Java
    * Obviously data syncronization would be instant
    * Output may look awful

### Internal Handling:
* Each section has its own 'pane', which consists of server- and client-side logic code, media files, and rendering code.
