from ..classes import Action
from . import kbdctypes
import time
import random
import datetime
import asyncio
from copy import deepcopy


class PressKey(Action):
    name = "PressKeyHandler"
    config_vars = Action.config_vars.copy()
    config_vars.update({
        "sequence": ["g", "LMB"],
        "interval": 1
    })

    def __init__(self, key_callback):
        super().__init__(key_callback)

    async def do(self):
        for i in self.config_vars["sequence"]:
            await kbdctypes.PressAndRelease(i)
            await asyncio.sleep(self.config_vars["interval"])
