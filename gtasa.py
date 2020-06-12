import kbdctypes
import time

#https://www.ign.com/wikis/grand-theft-auto-san-andreas/Cheat_Codes_and_Secrets#GTA_San_Andreas_PC_Cheat_Codes
#https://cyber.sports.ru/tribuna/blogs/picniconhardline/2405823.html

def enter_cheat(cheat):
    vis_format = "Interactive cheat {} activated!"
    vis_file_path = "gtasaviz.txt"
    with open(vis_file_path, "w") as vfout:
            vfout.write(vis_format.format(cheat))

    kbdctypes.BlockInput(True)
    for i in range(256):
        kbdctypes.ReleaseKey(i)

    for i in cheat:
        kbdctypes.PressAndRelease(i, 0.03)
    kbdctypes.BlockInput(False)

    time.sleep(4)
    with open(vis_file_path, "w") as vfout:
        vfout.write(" ")


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
