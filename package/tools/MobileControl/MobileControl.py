#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import uiautomator2 as u2
import time

from package.config import MobileConfig


class MobileControl:
    """手机控制"""
    APP_ALIPAY = 'Alipay'
    APP_TAOBAO = 'Taobao'
    APP_JD = 'JD'

    def __init__(self):
        self.device = None

    def connect(self, ip, delay=5):
        """链接手机"""
        print("连接手机" + str(ip))
        if isinstance(ip, str) and len(ip) > 0:
            self.device = u2.connect(ip)
        else:
            self.device = u2.connect()
        time.sleep(delay)

    def home(self, delay=3):
        """回到主界面"""
        self.device.press('home')
        time.sleep(delay)

    def back(self, delay=3):
        """回到主界面"""
        self.device.press('back')
        time.sleep(delay)

    def app_start(self, app, delay=12):
        """打开app"""
        print("打开APP：" + app)
        app_package = MobileConfig.app_package(app)
        if app_package:
            self.device.app_start(app_package)
            time.sleep(delay)

    def app_stop(self, app, delay=3):
        """打开app"""
        print("关闭APP：" + app)
        app_package = MobileConfig.app_package(app)
        if app_package:
            self.device.app_stop(app_package)
            time.sleep(delay)
