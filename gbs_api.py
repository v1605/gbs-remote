import requests
from menu_controller import MenuItem

slots = [
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-', '.', '_', '~', '(', ')', '!', '*', ':', ','
    ]
    

class GbsApi:
    
    def __init__(self, app_config):
        self.app_config = app_config
        
    def load_options(self):
        try:
            url="http://" + self.app_config['hostname'] + "/bin/slots.bin"
            r = requests.get(url, timeout=100)
            options = list()
            while True:
                chunk  = r.raw.recv(32)
                if not chunk:
                    break
                name = str(chunk[0:25], 'utf-8').split('\x00')[0].strip()
                code = slots[chunk[28]]
                options.append(MenuItem(name, code))
                if name == "Empty":
                    break
            r.close()
            return options
        except:
            return []
    
    def set_option(self, id_code):
        slot_url="http://" + self.app_config['hostname'] + "/slot/set?slot=" + id_code
        apply_url = "http://" + self.app_config['hostname'] + "/uc?3"
        try:
            requests.get(slot_url, data=None, timeout=10).close()
            requests.get(apply_url, data=None, timeout=10).close()
        except:
            print("Could not update")
        
    def get_url(self):
        return "http://" + self.app_config['hostname']
        
            
        