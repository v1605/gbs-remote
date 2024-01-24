import json

configFile = "settings.json"
def load_config():
    try:
        with open(configFile, "r") as f:
            return json.load(f)
    except:
        defaultConfig = {
            "hostname": "gbscontrol"
        }
        save_config(defaultConfig)
        return defaultConfig

def save_config(conf):
    with open(configFile, "w") as outfile:
        json.dump(conf, outfile)
