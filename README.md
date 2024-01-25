# gbs-remote
A wifi pico w remote for the gbs-control

## How to build your own
1. Aquire a Raspberry Pi Pico W (with headers if you don't want to solder).
2. Aquire a 1.3 WaveShare LCD (docs: https://www.waveshare.com/wiki/Pico-LCD-1.3) (eg. https://www.aliexpress.us/item/3256802431350939.html). Attach to the pico.
3. Put the Pi into boot mode (hold the boot button while connecting to a pc) and copy the lasted uf2 build to the pico.

## Configuration
On first boot, the remote will boot into an access point mode. The remotes ssid and password will display on screen. Once connected, navigate to the configutation page (http://192.168.4.1) and enter you wifi credentials (your remote and gbscontrol must be on the same network). If successful, the remote will reboot. The configuration page will be available on the device from your network to configure the gbscontrol hostname, which defaults to gbscontrol.

## Operation
Once connected and the gbscontrol's hostname is configured, the presets will disaply on screen. To select a preset, press the white button next to the option. Use the up and down directions of the joystick to scroll through the availble presets. The left and right directions toggle a information screen displaying the links to the remote's configuration page and the gbscontrol's ui. Pressing the center of the joystick will reload the presets from the gbscontrol.
