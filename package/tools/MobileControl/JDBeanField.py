#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import time
import random

from package.tools.MobileControl.MobileControl import MobileControl


class JDBeanField(MobileControl):
    """京东种豆得豆"""
    SCAN_TASK = [
        # '去签到',
        '去逛逛',
        '赢电竞椅',
        '去玩玩',
        '去购物',
    ]
    COLLECT_TASK = [
        '每日签到',
        '点击领取',
        '好友帮收'
    ]

    def open_bean_field(self, delay=10):
        """打开种豆得豆"""
        print("打开种豆得豆")
        # self.device(text="我的").click_exists(timeout=2)
        # time.sleep(2)
        # # 滑动页面
        # self.device.swipe(500, 1115, 500, 800)
        # self.device(text="种豆得豆").click_exists(timeout=2)
        # time.sleep(delay)
        self.device(text="领京豆").click_exists(timeout=2)
        time.sleep(delay)
        self.device.click(0.906, 0.508)
        time.sleep(delay)
        # 收京豆
        self.device.click(0.568, 0.606)
        time.sleep(2)
        self.device(text="收下京豆").click_exists(timeout=2)

    def collect(self, delay=1):
        """领取"""
        for collect_task_str in JDBeanField.COLLECT_TASK:
            print(collect_task_str)
            if self.device(text=collect_task_str).exists:
                self.device(text=collect_task_str).click()
                time.sleep(delay)

    def scan_shop(self, delay=2):
        """浏览店铺"""
        print('浏览店铺')
        i = 0
        while self.device(text="进店并关注").exists:
            self.device(text="进店并关注").click_exists(timeout=2)
            time.sleep(random.randint(8, 12))
            self.back()
            i += 1
            if i > 10:
                break
        time.sleep(delay)

    def open_task_page(self, delay=2):
        """打开任务列表"""
        print('打开任务列表')
        if self.device(text="更多任务 ").exists:
            self.device(text="更多任务 ").click_exists(timeout=2)
            time.sleep(delay)

    def handle_scan(self):
        """浏览任务"""
        print('处理浏览任务')
        i = 0
        while True:
            no_scan_task = True
            for scan_task_str in JDBeanField.SCAN_TASK:
                if self.device(text=scan_task_str).exists:
                    no_scan_task = False
                    self.device(text=scan_task_str).click()
                    time.sleep(random.randint(8, 12))
                    if self.device(text="活动已结束"):
                        self.device.click(0.157, 0.044)
                        continue
                    # 关注店铺
                    if self.device(text="进店并关注").exists:
                        self.scan_shop()
                    for j in range(3):
                        if not self.device(text="豆苗成长值").exists:
                            self.back()
                    i += 1
            if no_scan_task or i > 10:
                break

    def close_task_page(self):
        """关闭任务页"""
        print('关闭任务页')
        self.device.click(991, 370)

    def choose_goods(self):
        """挑选商品"""
        print('挑选商品')
        if self.device(text='去挑选').exists:
            self.device(text='去挑选').click_exists(timeout=2)
            time.sleep(5)
            for i in range(10):
                if self.device(text='x6').exists:
                    break
                self.device.click(0.765, 0.618)
                time.sleep(6)
                self.back()
                self.device.swipe(800, 900, 50, 900)
                time.sleep(1)
            self.back()

    def collect_nutrient_solution(self, delay=2):
        """收集浏览任务营养液"""
        print('收集浏览任务营养液')
        while self.device(text="x1").exists\
                or self.device(text="x2").exists\
                or self.device(text="x3").exists\
                or self.device(text="x4").exists\
                or self.device(text="x5").exists\
                or self.device(text="x6").exists:
            self.device(text="x1").click_exists(timeout=0.5)
            self.device(text="x2").click_exists(timeout=0.5)
            self.device(text="x3").click_exists(timeout=0.5)
            self.device(text="x4").click_exists(timeout=0.5)
            self.device(text="x5").click_exists(timeout=0.5)
            self.device(text="x6").click_exists(timeout=0.5)
            time.sleep(1)
        time.sleep(delay)

    def handle_task(self):
        """处理任务"""
        # 点击领取
        self.collect()
        # 打开任务页
        self.open_task_page()
        # 处理浏览任务
        self.handle_scan()
        # 挑选商品
        self.choose_goods()
        # 关闭任务页
        self.close_task_page()
        # 收集浏览任务营养液
        self.collect_nutrient_solution()

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
        # 打开种豆得豆
        self.open_bean_field()
        # 处理任务
        self.handle_task()
        # 关闭京东
        self.app_stop(MobileControl.APP_JD)
