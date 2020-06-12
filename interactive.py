#!/usr/bin/env python3


import sys
import socketio
import json
import configparser
import os
import kbdctypes
import time
import random
import datetime
#import gtasa
import requests


CWD = os.path.dirname(os.path.abspath(__file__))

CONFIG_PATH = os.path.join(CWD, "config.json")
CONFIG = json.load(open(CONFIG_PATH))

SECRETS_PATH = os.path.join(CWD, "secrets.json")
SECRETS = json.load(open(SECRETS_PATH))


sio_da = socketio.Client()
sio_t_cp = socketio.Client()


def update_config():
    global CONFIG
    CONFIG = json.load(open(CONFIG_PATH))


def handler_press_G():
    for i in CONFIG["press_G_settings"]["sequence"]:
        kbdctypes.PressAndRelease(i)
        time.sleep(CONFIG["press_G_settings"]["interval"])


def handler_press_random():
    handler_config = CONFIG["press_random_settings"]
    random_keys = handler_config["random_keys"]
    vis_file_path = handler_config["visualiser_file"]

    vis_format = "Random keys interactive! Pressed '{}' for {} seconds. Next key is '{}' in {} seconds"

    random_key = random.choice(random_keys)
    start_time = datetime.datetime.now()

    while (datetime.datetime.now() - start_time) < datetime.timedelta(seconds=handler_config["len"]):
        next_random_key = random.choice(random_keys)
        duration = random.uniform(handler_config["press_len_lo"], handler_config["press_len_hi"])
        interval = random.randint(handler_config["interval_lo"], handler_config["interval_hi"])

        with open(vis_file_path, "w") as vfout:
            vfout.write(vis_format.format(random_key, round(duration, 2), next_random_key, interval))

        kbdctypes.PressAndRelease(random_key, duration)
        time.sleep(interval - duration)
        random_key = next_random_key

    with open(vis_file_path, "w") as vfout:
        vfout.write(" ")

"""
def gtasa_random_cheat():
    while True:
        a = random.choice(list(CONFIG["price_handlers"].keys()))
        if a.startswith("gtasa."):
            eval(f"{a}()")
            break
"""

class Donation:
    def __init__(self, message):
        self.message = message
        self.additional_data = json.loads(self.message["additional_data"])
        self.amount = self.message["amount_main"]
        self.username = self.message["username"]

    def __str__(self):
        return f"{self.amount}"


class UnknownMessage:
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f"{self.message}"


@sio_da.on("donation")
def on_message(data_str):
    update_config()
    data = json.loads(data_str)
    print(data, file=sys.stderr)
    if str(data["alert_type"]) == "1":
        for k, price in CONFIG["price_handlers"].items():
            if Donation(data).amount == price:
                eval(f"{k}()")
    else:
        #print(UnknownMessage(data))
        pass


def connect_da():
    uri = CONFIG["donationalerts_server"]
    sio_da.connect(uri)
    sio_da.emit('add-user', {'token': SECRETS["donationalerts_token"], 'type': 'alert_widget'})
    print(f"Connected to donations alerts server {uri}")


def main():
    connect_da()


if __name__ == "__main__":
    main()
