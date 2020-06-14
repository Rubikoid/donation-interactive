from . import kbdctypes
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
