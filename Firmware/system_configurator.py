from json import dump
from json import load


def default_perl_config():
    return {
        "intensity":{
            "screen":0,
            "timer":0,
            "scorer":0
            },
        "mute":False
        }


def read_perl_config():
    try:
        file = open("perl_config.json", "r")
    except:
        write_perl_config(restore=True)
        return default_perl_config()
    else:
        data = load(file)
        file.close()
        return data


def write_perl_config(perl=None, restore=False):
    data = default_perl_config()
    if not restore:
        data["intensity"]["screen"] = perl.screen._intensity
        data["intensity"]["timer"] = perl.timer._intensity
        data["intensity"]["scorer"] = perl.scorer._intensity
        data["mute"] = perl.buzzer.mute
    with open("perl_config.json", "w") as file:
        dump(data, file)
    