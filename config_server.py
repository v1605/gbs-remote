from microdot import Microdot, send_file, Request, Response, redirect
from wifimgr import WifiManager
from menu_controller import MenuController
from gbs_api import GbsApi
import vga2_8x16 as small_font
import config_manager
import tft_config
import st7789
import utime

connected = False
Request.max_content_length = 1 * 1024 * 1024

def run():
    app = Microdot()
    tft = tft_config.config(1)
    tft.init()
    tft.fill(st7789.BLACK)
    config = config_manager.load_config()
    gbs_api = GbsApi(config)
    menu = MenuController(tft, gbs_api)
    wifiManager = WifiManager(menu)
    connected = wifiManager.get_connection() is not None
    if connected:
        menu.ip = wifiManager.get_connection().ifconfig()[0]
        menu.reload_options()
    
    @app.route('/')
    @app.route('')
    def index(request):
        return redirect('/static/index.html')
    
    @app.route('/static/<path:path>')
    def static(request, path):
        if '..' in path:
            # directory traversal is not allowed
            return 'Not found', 404
        print('static/' + path)
        return send_file('static/' + path, max_age=3600)
    
    
    @app.route('/api/updateWifi', methods=["POST"])
    def set_network_config(request):
        global connected
        ssid = request.json["ssid"]
        password = request.json["password"]
        connected = wifiManager.save_connect(ssid, password)
        if connected:
            menu.ip = wifiManager.get_connection().ifconfig()[0]
            menu.reload_options()
        return str(connected)
        
    @app.route('/api/hasWifi')
    def is_connected(request):
        return str(connected)
    
    @app.route('/api/settings', methods=["GET"])
    def get_settings(request):
        return Response(config)
    
    @app.route('/api/settings', methods=["POST"])
    def update_settings(request):
        print(request.json)
        hostname = request.json['hostname'].strip()
        if len(hostname) > 0:
            config["hostname"] = hostname
            if connected:
                menu.ip = wifiManager.get_connection().ifconfig()[0]
                menu.reload_options()
        config_manager.save_config(config)
    
    app.run(port=80)