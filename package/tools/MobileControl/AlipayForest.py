#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import time
import random

from package.tools.MobileControl.MobileControl import MobileControl


class AlipayForest(MobileControl):
    """支付宝蚂蚁森林"""
    collectEndSign = [
        '返回我的森林',
        '返回蚂蚁森林>',
        '返回蚂蚁森林 >',
    ]

    def open_forest(self, delay=15):
        """打开蚂蚁森林"""
        print("打开蚂蚁森林")
        self.device(text="蚂蚁森林").click_exists(timeout=5)
        time.sleep(delay)

    def collect_entry(self, cnt):
        """收集能量"""
        print("开始第%d次收集能量" % cnt)
        # 开始扫描点击有能力出现的区域
        for x in range(150, 950, 120):
            for y in range(550, 850, 120):
                if self.device(text='帮好友复活能量').exists and self.device(text='关闭').exists:
                    self.device(text='关闭').click_exists(timeout=1)
                    time.sleep(1)
                if self.device(text='蚂蚁森林种树攻略').exists:
                    self.back()
                self.device.click(x + random.randint(10, 20), y + random.randint(10, 20))
                if 1 != cnt:
                    time.sleep(0.01)
                    self.device.click(0.501, 0.799)
                time.sleep(0.01)
                if cnt != 1:
                    self.device.click(536, 1816)

    def find_entry(self):
        """点击找能量按钮"""
        a = self.device(resourceId="J_tree_dialog_wrap").bounds()
        self.device.click(1000, a[3] - 80)  # 找能量按钮的坐标

    def is_all_collect(self):
        """判断是否已收集完全"""
        for end_sign in AlipayForest.collectEndSign:
            if self.device(text=end_sign).exists(timeout=3):
                return True
        return False

    def back_to_forest(self, delay=5):
        """返回蚂蚁森林主页"""
        for end_sign in AlipayForest.collectEndSign:
            if self.device(text=end_sign).click_exists(timeout=3):
                time.sleep(delay)

    def open_task_page(self, delay=2):
        """打开任务页面"""
        print('打开任务页面')
        self.device.click(0.346, 0.644)
        time.sleep(delay)

    def receive_reward(self):
        """领取奖励"""
        for i in range(3):
            if self.device(text="立即领取", clickable=True).exists:
                self.device(text="立即领取", clickable=True).click_exists(timeout=2)
                time.sleep(1)

    def has_entry_rain_task(self):
        """判断是否有天天能量雨任务需处理"""
        print('判断是否有天天能量雨任务需处理')
        return self.device(text='去拯救').exists

    def open_entry_rain_task(self, delay=5):
        """打开天天能量雨任务"""
        print('打开天天能量雨任务')
        self.device(text='去拯救').click_exists(timeout=2)
        time.sleep(delay)

    def start_entry_rain_task(self, delay=0.5):
        """开始天天能量雨任务"""
        print('开始天天能量雨任务')
        self.device.click(503, 1438)
        time.sleep(3 + delay)

    def collect_entry_rain(self):
        """收集能量雨，任务持续10秒钟"""
        start_time = time.time()
        while True:
            # 开始扫描点击有能力出现的区域
            for x in range(150, 1000, 150):
                for y in range(550, 850, 150):
                    self.device.click(x, y)
            if time.time() - start_time > 10:
                break

    def entry_rain_task_handled(self):
        """判断是否有已处理天天能量雨任务"""
        print('判断是否有已处理天天能量雨任务')
        return self.device(text='邀请助力，再来一次').exists

    def handle_entry_rain_task(self):
        """处理天天能量雨任务"""
        if not self.has_entry_rain_task():
            print('无需处理天天能量雨任务')
            return
        self.open_entry_rain_task()
        if self.entry_rain_task_handled():
            self.back()
            return
        self.start_entry_rain_task()
        self.collect_entry_rain()
        self.back()

    def scan_help(self):
        pass

    def handle_task(self):
        """处理任务"""
        # 打开任务页面
        self.open_task_page()
        # 领取奖励
        self.receive_reward()
        # 滑动任务列表
        self.device.swipe(500, 1715, 500, 820)
        # 领取奖励
        self.receive_reward()
        # 天天能量雨任务
        # self.handle_entry_rain_task()

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
        # 打开蚂蚁森林
        self.open_forest()
        # 巡护
        self.scan_help()
        # 收集能量
        cnt = 1
        while True:
            self.collect_entry(cnt)
            self.find_entry()
            if self.is_all_collect():
                self.back_to_forest()
                print('收集完成')
                break
            if cnt > 60:
                self.back()
                break
            cnt += 1
        # 处理任务
        self.handle_task()
        # 关闭支付宝
        self.app_stop(MobileControl.APP_ALIPAY)
