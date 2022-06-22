#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import time

from package.tools.MobileControl.MobileControl import MobileControl


class JDShopUnsubscribe(MobileControl):
    """京东店铺取消关注"""

    def handle_task(self, delay=3):
        """处理任务"""
        print('京东店铺取消关注')
        self.device(text="我的").click_exists(timeout=2)
        time.sleep(5)
        self.device(text="店铺关注").click_exists(timeout=2)
        time.sleep(5)
        while self.device(text="编辑").exists:
            self.device(text="编辑").click_exists(timeout=2)
            time.sleep(3)
            self.device(text="全选").click_exists(timeout=2)
            time.sleep(2)
            elems = self.device.xpath("//*[@text='取消关注']").all()
            elems.reverse()
            elems[0].click()
            time.sleep(2)
            self.device(text="确定").click_exists(timeout=2)
            time.sleep(2)
        time.sleep(delay)

    def start_task(self, ip):
        """开始执行任务"""
        # 链接手机
        self.connect(ip)
        # 回到主页面
        self.home()
        # 关闭支付宝
        self.app_stop(MobileControl.APP_JD)
        # 打开支付宝
        self.app_start(MobileControl.APP_JD)
        # 处理任务
        self.handle_task()
        # 关闭支付宝
        self.app_stop(MobileControl.APP_JD)
