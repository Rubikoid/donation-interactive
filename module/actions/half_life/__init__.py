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


class HLRemoteConsole(object):
    def __init__(self):
        self.writer = None

    async def init(self, exe_name, hook):
        try:
            pid = injector.get_pid(exe_name)
        except Exception:
            print("[x] HL injection not found {exe_name}")
            return
        injector.inject_to_process(pid, hook)
        await asyncio.sleep(5)
        reader, writer = await asyncio.open_connection("127.0.0.1", 9998)
        self.reader: asyncio.StreamReader = reader
        self.writer: asyncio.StreamWriter = writer
        print("Connection ok")
        self.writer.write(f"sv_cheats 1".encode())
        # self.writer.write(f"developer 1")
        await self.writer.drain()

    async def destroy(self):
        if self.writer is not None:
            self.writer.close()


hlRemConsole = None


class HalfLifeCommand(Action):
    """HalfLife handler

    Config:
    ---
    _
    """

    config_vars = Action.config_vars.copy()
    config_vars.update({
        'type': 'HalfLifeCommand',
        'name': 'HalfLifeCommand_name',

        'exe_name': 'hl.exe',
        'hook_path': "D:\\Dsct\\Progs\\donation-interactive\\module\\actions\\half_life\\hook\\hook\\Debug\\hook.dll",
        "commands": [
            "sv_gravity 200",
            "_sleep 10",
            "sv_gravity 800"
        ],
        "amount": 1337
    })

    def __init__(self, key_callback):
        super().__init__(key_callback)

    async def init(self):
        global hlRemConsole
        if hlRemConsole is None:
            hlRemConsole = HLRemoteConsole()
            await hlRemConsole.init(self.config_vars["exe_name"], self.config_vars["hook_path"])

    async def destroy(self):
        global hlRemConsole
        if hlRemConsole is not None:
            await hlRemConsole.destroy()
            hlRemConsole = None

    async def writer_wrapper(self, cmds: list):
        for i in cmds:
            hlRemConsole.writer.write(i.encode())
        await hlRemConsole.writer.drain()

    async def do(self, donation: Donation):
        if donation.amount != self.config_vars["amount"]:
            return
        cmd = self.config_vars["commands"]
        await self.key_callback([f"Running HL commands {', '.join(cmd)}"])
        for i in cmd:
            if "_sleep" in i:
                await asyncio.sleep(float(i.split(' ')[1]))
            else:
                await self.writer_wrapper([
                    # f"say running {i};",
                    f"{i};"
                ])


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
