#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import time

import pykeyboard.mac
import pymouse.mac

from package.tools.SystemInput.Code import *


class MouseCommand:
    """mouse command class"""
    # 按键延时
    click_key_delay = 0.1
    # 鼠标
    mouse = pymouse.mac.PyMouse()
    # 键盘
    keyboard = pykeyboard.mac.PyKeyboard()

    @staticmethod
    def get_point():
        """get mouse current point (x,y)"""
        return MouseCommand.mouse.position()

    @staticmethod
    def move_to(x, y):
        """mouse move to point (x,y)"""
        MouseCommand.mouse.move(x, y)

    @staticmethod
    def left_click(x, y):
        """mouse left click on point (x,y)"""
        if x is not None and y is not None:
            MouseCommand.mouse.click(x, y)
            time.sleep(MouseCommand.click_key_delay)

    @staticmethod
    def right_click(x, y):
        """mouse right click on point (x,y)"""
        if x is not None and y is not None:
            MouseCommand.mouse.press(x, y, 2)
            time.sleep(MouseCommand.click_key_delay)
            MouseCommand.mouse.release(x, y, 2)

    @staticmethod
    def key_input(key):
        """keyboard click on key"""
        if key in MULTI_KEY_MAP:
            MouseCommand.multi_key_input(MULTI_KEY_MAP[key])
        else:
            MouseCommand.keyboard.press_key(key)
            MouseCommand.keyboard.release_key(key)

    @staticmethod
    def multi_key_input(keys):
        """keyboard multi click on keys"""
        if keys is None or not isinstance(keys, list) or len(keys) == 0:
            return
        if isinstance(keys[0], list):
            for key in keys:
                MouseCommand.multi_key_input(key)
        for key in keys:
            MouseCommand.keyboard.press_key(key)
        for key in keys:
            MouseCommand.keyboard.release_key(key)
        time.sleep(MouseCommand.click_key_delay)

    @staticmethod
    def str_input(string):
        """输入字符串"""
        for char in string:
            MouseCommand.key_input(char)
