#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import time

from package.tools.MobileControl.MobileControl import MobileControl


class AlipayFarm(MobileControl):
    """支付宝蚂蚁庄园"""
    KickOutPos = [
        {'x': 0.366, 'y': 0.714},
        {'x': 0.202, 'y': 0.586},
    ]

    def open_farm(self, delay=10):
        """打开蚂蚁庄园"""
        print("打开蚂蚁庄园")
        self.device(text="蚂蚁庄园").click()
        time.sleep(delay)

    def open_feed_task(self, delay=2):
        """打开领饲料页面"""
        print("打开领饲料页面")
        self.device.click(370, 1733)
        time.sleep(delay)

    def feed(self, delay=1):
        """喂饲料"""
        print("喂饲料")
        self.device.click(0.859, 0.905)
        time.sleep(delay)

    def kick_out(self, delay=1):
        """赶小鸡"""
        print("赶小鸡")
        for pos in AlipayFarm.KickOutPos:
            self.device.click(**pos)
            time.sleep(2)
        time.sleep(delay)

    def start_task(self, ip):
        """开始执行任务"""
        # 链接手机
        self.connect(ip)
        # 回到主页面
        self.home()
        # 关闭支付宝
        self.app_stop(MobileControl.APP_ALIPAY)
        # 打开支付宝
        self.app_start(MobileControl.APP_ALIPAY)
        # 打开蚂蚁庄园
        self.open_farm()
        # 喂饲料
        self.feed()
        # 赶小鸡
        self.kick_out()
        # 关闭支付宝
        self.app_stop(MobileControl.APP_ALIPAY)
