from . import random_keys
from . import press_x
from . import gtasa
from .half_life import HalfLifeCommand

actions = {
    "RandomKeysHandler": random_keys.RandomKeysHandler,
    "PressKeyHandler": press_x.PressKey,
    "HalfLifeCommand": HalfLifeCommand,
}  # TODO: fix that WTF
