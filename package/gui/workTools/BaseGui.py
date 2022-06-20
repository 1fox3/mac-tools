#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import tkinter


class BaseGui:
    """常用的字符串处理"""

    def __init__(self, root_tk):
        """首页初始化"""
        self.rootTk = tkinter.Frame(root_tk)

    def hide(self):
        """页面隐藏"""
        self.rootTk.destroy()
