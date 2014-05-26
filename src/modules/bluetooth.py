import sys
import render

try:
    import bluetooth

    bluetooth_available = True
except ImportError:
    bluetooth_available = False


class BluetoothModule(render.Module):
    def __init__(self, context):
        render.Module.__init__(self, context)
        self.status_label = render.OutlinedTextImg(color="#8888ff", outlinesize=2, size=20)
        try:
            self.bluetooth_address = context.config.get("Informant", "bluetooth")
            if len(self.bluetooth_address) == 0:
                self.bluetooth_address = None
        except:
            self.bluetooth_address = None
        # hack to make scanning happen soon after boot (but not directly at boot)
        # will be removed after threading implemented
        self._i = 85
        # 0=scan failed, 1=not found, 2=found
        self.bluetooth_device_found = -1

    def scan(self):
        if not bluetooth_available or self.bluetooth_address is None:
            return
        try:
            result = bluetooth.lookup_name(self.bluetooth_address, timeout=5)
            if result is None:
                self.bluetooth_device_found = 1
            else:
                self.bluetooth_device_found = 2
        except Exception as e:
            self.bluetooth_device_found = "Unexpected error: " + str(e)

    def render(self, screen, context):
        self._i += 1
        #scan every 3 minutes
        if self._i > 3 * 30:
            self._i = 0
            self.scan()

        str = self.bluetooth_device_found
        if not bluetooth_available:
            str = "BT Unavailable"
        elif self.bluetooth_device_found == 0:
            str = "BT Scan failed (%s)" % self.bluetooth_address
        elif self.bluetooth_device_found == 1:
            str = "BT Not found"
        elif self.bluetooth_device_found == 0:
            str = "BT Device found"

        self.status_label.render(screen, 300, context.height - 50, str)
