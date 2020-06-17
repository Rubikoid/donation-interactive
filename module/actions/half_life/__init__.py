from copy import deepcopy
import asyncio
import datetime
import random
import time

if __name__ == "__main__":
    import sys  # noqa
    sys.path.append("../../")  # noqa
    from classes import Action, Donation
    import injector
else:
    from ...classes import Action, Donation
    from . import injector


class HalfLifeCommand(Action):
    """empty

    Config:
    ---
    _
    """

    config_vars = Action.config_vars.copy()
    config_vars.update({
        'type': 'HalfLifeCommand',
        'name': 'HalfLifeCommand_name',

        'exe_name': 'hl.exe',
        'hook_path': ".\\hook\\hook\\Debug\\hook.dll",
        'amount': 1337,
    })

    def __init__(self, key_callback):
        super().__init__(key_callback)

    async def init(self):
        try:
            pid = injector.get_pid(self.config_vars['exe_name'])
        except Exception:
            return
        injector.inject_to_process(pid, self.config_vars['hook_path'])
        await asyncio.sleep(5)
        reader, writer = await asyncio.open_connection("127.0.0.1", 9998)
        self.reader: asyncio.StreamReader = reader
        self.writer: asyncio.StreamWriter = writer
        print("Connection ok")

    async def destroy(self):
        self.writer.close()

    async def do(self, donation: Donation):
        if donation.amount < self.config_vars["amount"]:
            return
        await self.key_callback([f"Running HL command"])
        self.writer.write(f"echo TEST {donation.username} {donation.amount}".encode())
        self.writer.write(f"say TEST {donation.username} {donation.amount}".encode())
        await self.writer.drain()
        # await kbdctypes.PressAndRelease()


if __name__ == "__main__":
    test = HalfLifeCommand(lambda x: None)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test.init())

    def wakeup():
        loop.call_later(0.1, wakeup)

    async def kek():
        while True:
            await asyncio.sleep(15)
            don = Donation({
                'additional_data': "{}",
                'amount_main': random.randint(1337, 9000),
                'username': 'test'
            })
            await test.do(don)

    loop.call_later(0.1, wakeup)
    loop.create_task(kek())

    try:
        loop.run_forever()
    finally:
        loop.run_until_complete(test.destroy())
