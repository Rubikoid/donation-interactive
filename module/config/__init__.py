import os
import json


class ConfigManager(object):
    CWD = os.path.dirname(os.path.abspath(__file__))
    CONFIG_PATH = os.path.join(CWD, "config.json")
    SECRETS_PATH = os.path.join(CWD, "secrets.json")

    def __init__(self):
        self.load()

    def load(self):
        self.config = json.load(open(self.CONFIG_PATH))
        self.secrets = json.load(open(self.SECRETS_PATH))

    def save(self):
        json.dump(self.config, open(self.CONFIG_PATH, 'w'))
        json.dump(self.secrets, open(self.SECRETS_PATH, 'w'))
