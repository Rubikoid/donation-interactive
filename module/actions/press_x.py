from ..classes import Action, Donation
from . import kbdctypes
import time
import random
import datetime
import asyncio
from copy import deepcopy


class PressKey(Action):
    """Press keys action. Just press key combination.

    Config:
    ---
    sequence: List = ["g", "LMB"]
        List of keys sequence, that should press
    interval: float = 1
        interval between key press
    amount: int = 10
        Donation amount for action work
    """

    config_vars = Action.config_vars.copy()
    config_vars.update({
        'type': 'PressKeyHandler',
        'name': 'PressKeyHandler_name',

        "sequence": ["g", "LMB"],
        "interval": 1.0,
        "amount": 10
    })

    def __init__(self, key_callback):
        super().__init__(key_callback)

    async def do(self, donation: Donation):
        if donation.amount != self.config_vars["amount"]:
            return
        for i in self.config_vars["sequence"]:
            await self.key_callback([f"Pressed {i} as part of {self.config_vars['sequence']}"])
            await kbdctypes.PressAndRelease(i)
            await asyncio.sleep(self.config_vars["interval"])
