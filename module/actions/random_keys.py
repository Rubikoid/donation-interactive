from ..classes import Action
from . import kbdctypes
import time
import random
import datetime
import asyncio
from copy import deepcopy


class RandomKeysHandler(Action):
    name = "RandomKeyHandler"
    config_vars = Action.config_vars.copy()
    config_vars.update({
        "random_keys": ["q", "w", "e", "a", "s", "d"],
        "interval_lo": 1,
        "interval_hi": 4,
        "press_len_lo": 0.1,
        "press_len_hi": 1,
        "len": 30
    })

    def __init__(self, key_callback):
        super().__init__(key_callback)

    async def do(self):
        random_keys = self.config_vars["random_keys"]
        # vis_file_path = self.config_vars["visualiser_file"]

        vis_format = "Random keys interactive! Pressed '{}' for {} seconds. Next key is '{}' in {} seconds"

        random_key = random.choice(random_keys)
        start_time = datetime.datetime.now()

        while (datetime.datetime.now() - start_time) < datetime.timedelta(seconds=self.config_vars["len"]):
            next_random_key = random.choice(random_keys)
            duration = random.uniform(self.config_vars["press_len_lo"], self.config_vars["press_len_hi"])
            interval = random.randint(self.config_vars["interval_lo"], self.config_vars["interval_hi"])

            await self.key_callback([
                (random_key, round(duration, 2))
            ])
            # print(vis_format.format(random_key, round(duration, 2), next_random_key, interval))
            # with open(vis_file_path, "w") as vfout:
            #    vfout.write(vis_format.format(random_key, round(duration, 2), next_random_key, interval))

            await kbdctypes.PressAndRelease(random_key, duration)
            await asyncio.sleep(interval - duration)
            random_key = next_random_key

        # with open(vis_file_path, "w") as vfout:
        #    vfout.write(" ")
