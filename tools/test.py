#!/usr/bin/env python3 mkdir(): Permission denied
# -*-coding:utf-8 -*-
import time

from appscript import app, k
import email
import poplib
import locale
import sys
import pymouse
import pykeyboard

if __name__ == "__main__":
    m = pymouse.mac.PyMouse()
    pymouse.mac.PyMouseEvent()
    while True:
        print(m.position()[1])
        time.sleep(0.2)
    # m.press(500, 600, 1)
    # time.sleep(0.2)
    # m.release(500, 600, 1)
    # time.sleep(0.2)
    # m.press(500, 600, 2)
    # time.sleep(0.2)
    # m.release(500, 600, 2)
    # time.sleep(2)
    k = pykeyboard.mac.PyKeyboard()
    k.press_key()
    # k.press_key('function')