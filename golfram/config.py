import ConfigParser

_settings = {}

def load(filename):
    config = ConfigParser.RawConfigParser()
    config.read(filename)
    _settings['data_path'] = config.get('Settings', 'data_path')

def get(setting_name):
    return _settings[setting_name]
