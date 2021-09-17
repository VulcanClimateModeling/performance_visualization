
import json

CONFIG = None

def load_analysis_config(config_path):
    global CONFIG
    if CONFIG is not None:
        raise RuntimeError("Attempt to load configuration twice.")
    with open(config_path) as json_file:
        CONFIG = json.load(json_file)

def get_analysis_config():
    global CONFIG
    if CONFIG is None:
        raise RuntimeError("Attempt to get configuration before loading it.")
    return CONFIG