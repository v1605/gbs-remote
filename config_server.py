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
    menu.app_config = config
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
        hostname = request.json['hostname']
        if hostname is not None and len(hostname.strip()) > 0:
            config["hostname"] = hostname.strip()
            if connected:
                menu.ip = wifiManager.get_connection().ifconfig()[0]
                menu.reload_options()
        postUrl = request.json['postUrl']
        if postUrl is not None:
            config["postUrl"] = postUrl.strip() 
        config_manager.save_config(config)
        
    @app.route('/api/presets', methods=["GET"])
    def get_preset(request):
        options = list(map(lambda x: x.__dict__, gbs_api.load_options()))
        return Response(options)
    
    @app.route('/api/presets', methods=["POST"])
    def set_preset(request):
        code = ""
        if "id" in request.json:
            gbs_api.set_option(request.json["id"])
        else:
            options = gbs_api.load_options();
            name = request.json["display"].strip()
            found = None;
            try:
                found = next(option for option in options if option.display == name) #No default?
            except:
                pass
            if found is not None:
                gbs_api.set_option(found.id)
            else:
                return Response("Could not find option", 404)
        return Response("Updated option")
    app.run(port=80)