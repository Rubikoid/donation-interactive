from ..classes import Action
from . import kbdctypes
import time
import random
import datetime
from copy import deepcopy


class PressKey(Action):
    name = "PressKeyHandler"
    config_vars = Action.config_vars.copy()
    config_vars.update({
        "sequence": ["g", "LMB"],
        "interval": 1
    })

    def __init__(self):
        super().__init__()

    def do(self):
        for i in self.config_vars["sequence"]:
            kbdctypes.PressAndRelease(i)
            time.sleep(self.config_vars["interval"])
