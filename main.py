from Sparserestore.restore import restore_files, FileToRestore
from devicemanagement.constants import Device
from pymobiledevice3 import usbmux
from pymobiledevice3.lockdown import create_using_usbmux
import traceback

device = None

def connect_device():
    global device
    connected_devices = usbmux.list_devices()
    for current_device in connected_devices:
        if current_device.is_usb:
            try:
                ld = create_using_usbmux(serial=current_device.serial)
                vals = ld.all_values
                device = Device(
                    uuid=current_device.serial,
                    name=vals['DeviceName'],
                    version=vals['ProductVersion'],
                    model=vals['ProductType'],
                    locale=ld.locale,
                    ld=ld,
                    build=vals['BuildVersion']
                )
                print(f"Connected to {device.name} (iOS {device.version})")
            except Exception as e:
                print("Error connecting:")
                print(traceback.format_exc())

def overwrite():
    try:
        restore_files(files=[FileToRestore(
            contents=b"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>AllowPairing</key>
	<true/>
	<key>CloudConfigurationUIComplete</key>
	<true/>
	<key>ConfigurationSource</key>
	<integer>0</integer>
	<key>IsSupervised</key>
	<false/>
	<key>PostSetupProfileWasInstalled</key>
	<false/>
</dict>
</plist>""",
            restore_path="/var/containers/Shared/SystemGroup/systemgroup.com.apple.configurationprofiles/Library/ConfigurationProfiles/CloudConfigurationDetails.plist"
        )], reboot=True, lockdown_client=device.ld)
        
        print("MDM removed.")
    except Exception as e:
        print("Error restoring：")
        print(traceback.format_exc())


def main():
    connect_device()
    if device:
        overwrite()
    
    input("Enter to exit...")

if __name__ == "__main__":
    main()
