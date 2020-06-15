from ..classes import Action, Donation
from . import kbdctypes
import time
import random
import datetime
import asyncio
from copy import deepcopy


class RandomKeysHandler(Action):
    """Random key action. On donate, press random keys for random time.

    Config:
    ---
    random_keys: List = ["q", "w", "e", "a", "s", "d"]
        List of keys, that can be pressed
    interval_lo: int = 1
        minimum interval between keys press
    interval_hi: int = 4
        maximum interval between keys press
    press_len_lo: float = 0.1
        minimum key press duration
    press_len_hi: int = 1
        maximum key press duration
    len: int = 30
        time of action effect
    amount: int = 10
        Donation amount for action work
    """

    name = "RandomKeyHandler"
    config_vars = Action.config_vars.copy()
    config_vars.update({
        "random_keys": ["q", "w", "e", "a", "s", "d"],
        "interval_lo": 1,
        "interval_hi": 4,
        "press_len_lo": 0.1,
        "press_len_hi": 1,
        "len": 30,

        "amount": 10
    })

    def __init__(self, key_callback):
        super().__init__(key_callback)

    async def do(self, donation: Donation):
        if donation.amount != self.config_vars["amount"]:
            return
        random_keys = self.config_vars["random_keys"]

        random_key = random.choice(random_keys)
        start_time = datetime.datetime.now()

        while (datetime.datetime.now() - start_time) < datetime.timedelta(seconds=self.config_vars["len"]):
            next_random_key = random.choice(random_keys)
            duration = random.uniform(self.config_vars["press_len_lo"], self.config_vars["press_len_hi"])
            interval = random.randint(self.config_vars["interval_lo"], self.config_vars["interval_hi"])

            await self.key_callback([f"Pressed {random_key}, for {round(duration, 2)}"])

            await kbdctypes.PressAndRelease(random_key, duration)
            await asyncio.sleep(interval - duration)
            random_key = next_random_key
