#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import time
import random

from package.tools.MobileControl.MobileControl import MobileControl


class JDBean(MobileControl):
    """京东领京豆"""

    def open_bean(self, delay=10):
        """打开京豆"""
        print("打开京豆")
        self.device(text="领京豆").click_exists(timeout=2)
        time.sleep(delay)

    def sign_in(self, delay=1):
        """签到领京豆"""
        print("签到领京豆")
        self.device.click(0.501, 0.177)
        if not self.device(text="领京豆").exists:
            self.back()
        time.sleep(delay)
        # if self.device(text="签到领京豆").exists:
        #     self.device(text="签到领京豆").click_exists(timeout=2)
        #     time.sleep(delay)

    def open_task_page(self, delay=2):
        """打开任务页"""
        print("打开任务页")
        self.device.click(0.474, 0.517)
        time.sleep(delay)
        # 移动京豆领取升级任务
        # self.device.swipe(0.832, 0.51, 0.832, 0.314)
        # time.sleep(1)

    def handle_scan(self):
        """处理浏览任务"""
        print("处理浏览任务")
        # for i in range(20):
        #     if not self.device(text="购物返豆").exists:
        #         break
        #     self.device.click(0.842, 0.549)
        #     time.sleep(random.randint(8, 12))
        #     if self.device(text="京东超市").exists:
        #         self.open_bean()
        #         self.open_task_page()
        #     for j in range(3):
        #         if not self.device(text="购物返豆").exists:
        #             self.back()
        #         else:
        #             break
        task_num = 1
        while self.device(text="去完成").exists:
            print(task_num, end=' ')
            task_num += 1
            self.device(text="去完成").click()
            time.sleep(random.randint(8, 12))
            if self.device(text="去完成").exists or self.device(text="已完成").exists:
                # 关闭弹窗提示
                self.device.click(0.495, 0.742)
                time.sleep(2)
                continue
            for i in range(3):
                if not self.device(text="去完成").exists and not self.device(text="已完成").exists:
                    self.back(1)
            time.sleep(1)
            if task_num > 60:
                break

    def handle_task(self):
        """处理任务"""
        # 签到
        self.sign_in()
        # 打开任务页
        self.open_task_page()
        # 处理浏览任务
        self.handle_scan()

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
        # 打开京豆
        self.open_bean()
        # 处理任务
        self.handle_task()
        # 关闭京东
        self.app_stop(MobileControl.APP_JD)
