from . import random_keys
from . import press_x
from . import gtasa

actions = {
    random_keys.RandomKeysHandler.name: random_keys.RandomKeysHandler,
    press_x.PressKey.name: press_x.PressKey,
}  # TODO: fix that WTF
