#!/usr/bin/env python3

import atexit
import time
import threading
import asyncio
import websockets
import logging
from . import actions
from . import config
from . import donation_providers
from . import ui
from . import classes


class Main(object):
    """Main, god-like class for entire application

    """

    def __init__(self):
        self.conf_manager = config.ConfigManager()
        self.actions = []
        self.providers = []
        self.config_loader("actions", self.actions, actions.actions)
        self.config_loader("providers", self.providers, donation_providers.providers)
        self.clients = []

        self.start_server = websockets.serve(self.ws_handler, "localhost", 6789)
        asyncio.get_event_loop().run_until_complete(self.start_server)

        # atexit.register(self.closing_handler)

    def config_loader(self, collection_name, array_out, array_in):
        """Loads config."""
        secrets_hive = self.conf_manager.secrets[collection_name]
        for i in self.conf_manager.config[collection_name]:
            if i["name"] not in array_in:
                continue
            if array_in == donation_providers.providers:  # FIXME: shitty code
                var = array_in[i["name"]](self.provider_handler)
            else:
                var = array_in[i["name"]](self.key_handler)
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
        """Closing handler, stopps all providers and websocket server"""
        print("Stopping providers...")
        for i in self.providers:
            asyncio.get_event_loop().run_until_complete(i.disconnect())
        self.start_server.ws_server.close()

    async def provider_handler(self, data: classes.Donation):
        """Provider handler, get called by donation providers, on new donation"""
        print(f"New donation: {repr(data)}")
        for i in self.actions:
            asyncio.get_event_loop().create_task(i.do(data))

    async def key_handler(self, data: list):
        """Key handler, get called by actions, on keys update"""
        for i in data:
            for c in self.clients:
                await c.send(i)

    async def ws_handler(self, websocket, path):
        self.clients.append(websocket)
        async for message in websocket:
            pass

    def run(self):
        """Run everything"""
        for i in self.actions:
            print(f"Action: {i.__str__()}\n")
        print()
        for i in self.providers:
            print(f"Provider: {i.__str__()}\n")

        for i in self.providers:
            asyncio.get_event_loop().run_until_complete(i.connect())

        def wakeup():
            asyncio.get_event_loop().call_later(0.1, wakeup)

        print("Going to infinity loop...")
        asyncio.get_event_loop().call_later(0.1, wakeup)
        try:
            asyncio.get_event_loop().run_forever()
        finally:
            self.closing_handler()


def main():
    logging.getLogger("asyncio").setLevel(logging.DEBUG)
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
