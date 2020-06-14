#!/usr/bin/env python3

import atexit
import time
import threading
import asyncio
import websockets
from . import actions
from . import config
from . import donation_handlers
from . import ui
from . import classes


class Main(object):
    conf_manager = None

    def __init__(self):
        self.conf_manager = config.ConfigManager()
        self.actions = []
        self.providers = []
        self.config_loader("actions", self.actions, actions.actions)
        self.config_loader("providers", self.providers, donation_handlers.providers)
        self.clients = []

        self.start_server = websockets.serve(self.ws_handler, "localhost", 6789)
        asyncio.get_event_loop().run_until_complete(self.start_server)

        # atexit.register(self.closing_handler)

    def config_loader(self, collection_name, array_out, array_in):
        secrets_hive = self.conf_manager.secrets[collection_name]
        for i in self.conf_manager.config[collection_name]:
            if i["name"] not in array_in:
                continue
            if array_in == donation_handlers.providers:  # FIXME: shitty code
                var = array_in[i["name"]](self.provider_handler)
            else:
                var = array_in[i["name"]](self.action_handler)
            for config_name in var.config_vars:
                if config_name not in i:
                    continue
                var.config_vars[config_name] = i[config_name]

            for secr in secrets_hive:
                if secr["name"] == i["name"]:
                    for secret_name in var.secret_vars:
                        if secret_name not in secr:
                            continue
                        var.secret_vars[secret_name] = secr[secret_name]
                    break
            array_out.append(var)

    def closing_handler(self):
        print("DIEEEEEEEE")
        for i in self.providers:
            i.disconnect()

    async def provider_handler(self, data: classes.Donation):
        print(f"New donation: {repr(data)}")
        for i in self.actions:
            if i.config_vars["conditions"][0]["price"] == data.amount:
                print(f"Doing {i}")
                await i.do()
                break

    async def action_handler(self, data: list):
        for i in data:
            key, dur = i
            k = f"Pressed {key} for {dur}"
            print(k)
            for i in self.clients:
                await i.send(k)

    async def ws_handler(self, websocket, path):
        self.clients.append(websocket)
        async for message in websocket:
            pass

    def run(self):
        for i in self.actions:
            print(f"Action: {i.__str__()}")
        print()
        for i in self.providers:
            print(f"Provider: {i.__str__()}")

        # for i in actions.actions:
        #     print(f"test: {actions.actions[i].config_vars}")
        for i in self.providers:
            asyncio.get_event_loop().run_until_complete(i.connect())

        def wakeup():
            asyncio.get_event_loop().call_later(0.1, wakeup)

        def wat():
            print("I'm TRYING TO DIEEE")
            self.start_server.ws_server.close()
            asyncio.get_event_loop().stop()
            asyncio.get_event_loop().close()

        print("Going to infinity loop......")
        asyncio.get_event_loop().call_later(0.1, wakeup)
        asyncio.get_event_loop().run_forever()

        # self.sio_thread = threading.Thread(target=lambda: self.socketio.run(self.app))
        # self.app.run(debug=True)
        # self.sio_thread.run()


def main():
    m = Main()
    m.run()
    try:
        while True:
            print("I WANNA DIEEE")
            input()
    finally:
        m.closing_handler()


if __name__ == "__main__":
    main()
