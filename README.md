# gbs-remote

A wifi pico w remote for the [gbs-control](https://github.com/ramapcsx2/gbs-control) scaler.

![img](https://github.com/v1605/gbs-remote/assets/55302877/fa613fc9-b5e2-45a1-83d1-886393a13338)

## How to build your own
1. Aquire a Raspberry Pi Pico W (with headers if you don't want to solder).
2. Aquire a 1.3 WaveShare LCD (docs: https://www.waveshare.com/wiki/Pico-LCD-1.3) (eg link to purchase. https://www.aliexpress.us/item/3256802431350939.html).
3. Attach the lcd to the pico.
4. Put the Pi into boot mode (hold the boot button while connecting to a pc) and copy the lasted uf2 build to the pico.

## Configuration
On first boot, the remote will boot into an access point mode. The remotes ssid and password will display on screen. Once connected, navigate to the configutation page (http://192.168.4.1) and enter you wifi credentials (your remote and gbscontrol must be on the same network). If successful, the remote will reboot. The configuration page will be available on the device from your network to configure the gbscontrol hostname, which defaults to gbscontrol.

## Operation
Once connected and the gbscontrol's hostname is configured, the presets will disaply on screen. To select a preset, press the white button next to the option. Use the up and down directions of the joystick to scroll through the availble presets. The left and right directions toggle a information screen displaying the links to the remote's configuration page and the gbscontrol's ui. Pressing the center of the joystick will reload the presets from the gbscontrol.

##Development setup
If you want to contribute or tweak the code:
1. Either download the latest release or download the display firmware directly from the ST7789 Driver for MicroPython at https://github.com/russhughes/st7789_mpy
2. Flash the firmware to the pico.
3. Using a IDE like Thonny to copy micropython files to the pico.
