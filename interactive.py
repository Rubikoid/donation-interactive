#!/usr/bin/env python3

import module as m
import threading


def imp():
    x = m.main()
    x.run_configurator()
    # thr = threading.Thread(target=x.run_configurator)
    # thr.run()
    # x.run()


if __name__ == "__main__":
    imp()
