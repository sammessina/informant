import subprocess

from module import Module
import render


try:
    import bluetooth
    bluetooth_available = True
except ImportError:
    bluetooth = None
    bluetooth_available = False


class BluetoothModule(Module):
    def __init__(self, context):
        Module.__init__(self, context)
        self.monitor_is_on = True
        self.status_label = render.OutlinedTextImg(color="#8888ff", outlinesize=2, size=20)
        self.bluetooth_address = context.config.get("Informant", "bluetooth")
        if len(self.bluetooth_address) == 0:
            self.bluetooth_address = None
        # -1=scan failed, 0=not scanned, 1=not found, 2=found
        self.bluetooth_status = 0

    def _monitor_off(self):
        if self.monitor_is_on:
            subprocess.call("tvservice -o", shell=True)
            self.monitor_is_on = False

    def _monitor_on(self):
        if not self.monitor_is_on:
            subprocess.call("tvservice -p && chvt 6 && chvt 7", shell=True)
            self.monitor_is_on = True

    def update(self, context):
        if not bluetooth_available or self.bluetooth_address is None:
            return
        try:
            result = bluetooth.lookup_name(self.bluetooth_address, timeout=5)
            if result is None:
                self.bluetooth_status = 1
            else:
                self.bluetooth_status = 2
        except:
            self.bluetooth_status = -1

    def render(self, screen, context):
        if self.bluetooth_address is None:
            return

        bt_msg = ""
        if not bluetooth_available:
            bt_msg = "BT Software not installed"
        elif self.bluetooth_status == -1:
            bt_msg = "" # failed - missing hw?
        elif self.bluetooth_status == 0:
            bt_msg = "BT Scan pending"
        elif self.bluetooth_status == 1:
            bt_msg = "BT Not found"
        elif self.bluetooth_status == 2:
            bt_msg = "BT Device found"

        self.status_label.render(screen, 700, context.height - 50, bt_msg)
