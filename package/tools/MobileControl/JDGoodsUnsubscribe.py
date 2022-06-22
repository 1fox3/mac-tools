#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import time

from package.tools.MobileControl.MobileControl import MobileControl


class JDGoodsUnsubscribe(MobileControl):
    """京东商品取消收藏"""

    def handle_task(self, delay=3):
        """处理任务"""
        print('京东商品取消收藏')
        self.device(text="我的").click_exists(timeout=2)
        time.sleep(5)
        self.device(text="商品收藏").click_exists(timeout=2)
        time.sleep(5)
        while self.device(text="编辑").exists:
            self.device(text="编辑").click_exists(timeout=2)
            time.sleep(3)
            self.device.click(0.05, 0.954)
            time.sleep(2)
            for i in range(11):
                if 0 == i:
                    continue
                if self.device(text='取消收藏(' + str(i) + ')').exists:
                    self.device(text='取消收藏(' + str(i) + ')').click_exists(timeout=2)
                    time.sleep(3)
                    break
            self.device(text="确定").click_exists(timeout=2)
            time.sleep(2)
        time.sleep(delay)

    def start_task(self, ip):
        """开始执行任务"""
        # 链接手机
        self.connect(ip)
        # 回到主页面
        self.home()
        # 关闭京东
        self.app_stop(MobileControl.APP_JD)
        # 打开京东
        self.app_start(MobileControl.APP_JD)
        # 处理任务
        self.handle_task()
        # 关闭京东
        self.app_stop(MobileControl.APP_JD)
