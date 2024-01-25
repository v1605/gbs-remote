import vga2_8x16 as small_font
import network
import socket
import ure
import st7789
import machine
import utime

ap_ssid = "GbsRemote"
ap_password = "gbsremote1"
ap_authmode = 3  # WPA2

NETWORK_PROFILES = 'wifi.dat'

wlan_ap = network.WLAN(network.AP_IF)
wlan_sta = network.WLAN(network.STA_IF)

server_socket = None

class WifiManager:
    
    def __init__(self, menu):
        self._menu = menu;
        self.retry = 1
    
    def get_connection(self):
        """return a working WLAN(STA_IF) instance or None"""

        # First check if there already is any connection:
        if wlan_sta.isconnected():
            return wlan_sta
        self._menu.clear()
        self._menu.write("Starting wifi",20,20);
        connected = False
        try:
            # ESP connecting to WiFi takes time, wait a bit and try again:
            utime.sleep(3)
            if wlan_sta.isconnected():
                print('\nConnected. Network config: ', wlan_sta.ifconfig())
                return wlan_sta

            # Read known network profiles from file
            profiles = self.read_profiles()

            # Search WiFis in range
            wlan_sta.active(True)
            networks = wlan_sta.scan()

            AUTHMODE = {0: "open", 1: "WEP", 2: "WPA-PSK", 3: "WPA2-PSK", 4: "WPA/WPA2-PSK"}
            for ssid, bssid, channel, rssi, authmode, hidden in sorted(networks, key=lambda x: x[3], reverse=True):
                ssid = ssid.decode('utf-8')
                encrypted = authmode > 0
                print("ssid: %s chan: %d rssi: %d authmode: %s" % (ssid, channel, rssi, AUTHMODE.get(authmode, '?')))
                if encrypted:
                    if ssid in profiles:
                        password = profiles[ssid]
                        connected = self.do_connect(ssid, password)
                    else:
                        print("skipping unknown encrypted network")
                if connected:
                    break

        except OSError as e:
            print("exception", str(e))
        if not connected:
            self._menu.clear()
            self._menu.write("Could not connect",20,20);
            self._menu.write("Configure via web",20,38);
            self._menu.write("AP: " + ap_ssid ,20, 56);
            self._menu.write("Password: " + ap_password, 20,74);
            wlan_ap.config(ssid=ap_ssid, password=ap_password)
            wlan_ap.active(True)
        return wlan_sta if connected else None


    def save_connect(self, ssid, password):
        connected = self.do_connect(ssid, password)
        if connected:
            profiles = self.read_profiles()
            profiles[ssid] = password
            self.write_profiles(profiles)
            self._menu.clear()
            self._menu.write("Connected. Rebooting",20,20)
            utime.sleep_ms(600)
            machine.reset() #For some reason, requests does not like it when you don't power cycle?
        return connected

    def read_profiles(self):
        with open(NETWORK_PROFILES) as f:
            lines = f.readlines()
        profiles = {}
        for line in lines:
            ssid, password = line.strip("\n").split(";")
            profiles[ssid.strip()] = password.strip()
        return profiles


    def write_profiles(self, profiles):
        lines = []
        for ssid, password in profiles.items():
            lines.append("%s;%s\n" % (ssid, password))
        with open(NETWORK_PROFILES, "w") as f:
            f.write(''.join(lines))


    def do_connect(self, ssid, password):
        wlan_sta.active(True)
        password= self._unquote(password)
        print(ssid)
        print(password)
        if wlan_sta.isconnected():
            print('\nConnected. Network config: ', wlan_sta.ifconfig())
            return None
        print('Trying to connect to %s...' % ssid )
        wlan_sta.connect(ssid, password)
        for retry in range(200):
            connected = wlan_sta.isconnected()
            if connected:
                wlan_ap.active(False)
                wlan_ap.disconnect()
                break
            utime.sleep(0.1)
            print('.', end='')
            self._menu.loadingIncrement()
        if connected:
            print('\nConnected. Network config: ', wlan_sta.ifconfig())          
        else:
            print('\nFailed. Not Connected to: ' + ssid)
        return connected



    def _unquote(self, string):
        bits = string.split('%')

        res = bits[0]
        for item in bits[1:]:
            res = res + chr(int(item[:2], 16)) + item[2:]

        return res
