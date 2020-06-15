from ..classes import Action, Donation
from . import kbdctypes
import time
import random
import datetime
import asyncio
from copy import deepcopy


class ActionExample(Action):
    """Just press key example.

    Config:
    ---
    key: str = 'f'
        key, that will be pressed
    amount: int = 10
        Donation amount for action work
    """

    name = "ActionExample"
    config_vars = Action.config_vars.copy()
    config_vars.update({
        "key": ["f"],
        "amount": 10
    })

    def __init__(self, key_callback):
        super().__init__(key_callback)

    async def do(self, donation: Donation):
        if donation.amount != self.config_vars["amount"]:
            return
        await self.key_callback([f"Pressed {self.config_vars['key']}"])
        await kbdctypes.PressAndRelease()
