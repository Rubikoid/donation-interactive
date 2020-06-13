import kbdctypes
import time
import csv
import os

CHEATS = []

CWD = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(CWD, "gtasa.csv"), encoding='utf-8') as csvfile:
    cheatsreader = csv.DictReader(csvfile, delimiter=',')
    for cheat in cheatsreader:
        dc = dict(cheat)
        dc['price'] = int(dc['price'])
        CHEATS.append(dc)


def enter_cheat(cheat):
    vis_format = "Interactive cheat {} activated! {}"
    vis_file_path = os.path.join(CWD, "gtasaviz.txt")
    with open(vis_file_path, "w", encoding="utf-8") as vfout:
            vfout.write(vis_format.format(cheat['cheat'], cheat['description']))

    kbdctypes.BlockInput(True)

    for i in cheat['cheat']:
        kbdctypes.PressAndRelease(i, 0.02)
        time.sleep(0.02)
    time.sleep(0.02)
    kbdctypes.BlockInput(False)

    time.sleep(8)
    with open(vis_file_path, "w") as vfout:
        vfout.write(" ")


def universal_handler(donation_sum):
    for cheat in CHEATS:
        if cheat['price'] == donation_sum:
            enter_cheat(cheat)
            return True
    else:
        return False


"""
def handler_give_2_stars():
    enter_cheat("OSRBLHH")


def handler_clear_stars():
    enter_cheat("ASNAEB")


def handler_give_6_stars():
    enter_cheat("LJSPQK")


def handler_weapons_to_all():
    enter_cheat("FOOOXFT")


def handler_give_parachute():
    enter_cheat("AIYPWZQP")


def handler_make_fat():
    enter_cheat("BTCDBCB")


def handler_make_skinny():
    enter_cheat("KVGYZQK")


def handler_spawn_rhino():
    enter_cheat("AIWPRTON")


def handler_spawn_bloodring_banger():
    enter_cheat("CQZIJMB")


def handler_spawn_racecar():
    enter_cheat("PDNEJOH")


def handler_spawn_catafalque():
    enter_cheat("AQTBCODX")


def handler_spawn_stretch():
    enter_cheat("KRIJEBR")
"""