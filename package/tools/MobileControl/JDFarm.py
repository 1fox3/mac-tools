#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import time
import random

from package.tools.MobileControl.MobileControl import MobileControl


class JDFarm(MobileControl):
    """京东种豆得豆"""

    def open_farm(self, delay=3):
        """打开京东农场"""
        print("打开京东农场")
        self.device(text="领京豆").click_exists(timeout=2)
        time.sleep(delay)
        self.device.click(0.083, 0.512)
        time.sleep(5)
        self.device.click(0.506, 0.775)
        time.sleep(delay)

    def open_sign_page(self, delay=3):
        """打开签到页"""
        self.device.click(0.127, 0.723)
        time.sleep(delay)

    def handle_sign_task(self):
        """处理签到任务"""
        if self.device(text="签到领").exists:
            self.device(text="签到领").click_exists(timeout=2)
        if self.device(text="明日再来").exists:
            self.device(text="明日再来").click_exists(timeout=2)
        if self.device(text="领取惊喜礼包").exists:
            self.device(text="领取惊喜礼包").click_exists(timeout=2)
            if self.device(text="明日再来").exists:
                self.device(text="明日再来").click_exists(timeout=2)

    def close_sign_page(self, delay=2):
        """关闭签到页"""
        self.back()
        time.sleep(delay)

    def handle_sign(self):
        """处理签到任务"""
        # 打开签到页
        self.open_sign_page()
        # 处理签到任务
        self.handle_sign_task()
        # 关闭签到页
        self.close_sign_page()

    def open_paradise_page(self, delay=8):
        """打开东东乐园"""
        print('打开东东乐园')
        self.device.click(0.272, 0.473)
        time.sleep(2)
        # # 水果泡泡龙领水滴
        # self.device.click(0.241, 0.56)
        # time.sleep(15)
        # self.back()
        # self.device.click(0.241, 0.56)
        # time.sleep(1)
        # if self.device(text="水果泡泡龙").exists:
        #     self.back()
        # 滑动任务列表
        self.device.swipe(500, 600, 500, 1700)
        time.sleep(1)
        self.device.click(0.239, 0.262)
        time.sleep(delay)

    def handle_paradise_scan(self):
        """浏览任务"""
        print('处理浏览任务')
        self.device(text="快去抽奖").click_exists(timeout=2)
        task_num = 0
        for i in range(15):
            task_num = i
            if not self.device(text="去浏览").exists:
                break
            self.device(text="去浏览").click_exists(timeout=1)
            # self.device.click(0.832, 0.848)
            time.sleep(random.randint(8, 10))
            for j in range(3):
                self.back()
                if self.device(text="天天红包").exists:
                    break
            self.device(text="立即领取").click_exists(timeout=1)
            time.sleep(1)
            # 滑动任务列表
            self.device.swipe(0.832, 0.924, 0.832, 0.84)

        # 回到页面顶端
        for i in range(task_num):
            self.device.swipe(0.832, 0.84, 0.832, 0.924)

    def lucky_draw(self):
        """抽奖"""
        for i in range(15):
            self.device.click(0.501, 0.463)
            time.sleep(9)
            if not self.device(text="继续抽奖").exists:
                time.sleep(2)
                break
            self.device(text="继续抽奖").click_exists(timeout=2)

    def close_paradise_page(self, delay=2):
        """关闭任务页"""
        print('关闭任务页')
        self.back()
        time.sleep(1)
        self.device.click(0.239, 0.262)
        time.sleep(10)
        if self.device(text="天天红包").exists:
            self.back()
            time.sleep(1)
        self.back()
        time.sleep(delay)

    def open_task_page(self, delay=3):
        """打开任务列表"""
        print('打开任务列表')
        self.device.click(0.277, 0.72)
        time.sleep(delay)

    def handle_scan(self):
        """浏览任务"""
        print('处理浏览任务')
        for i in range(15):
            # 领按时奖励
            if self.device(text="去领取").exists:
                self.device(text="去领取").click_exists(timeout=1)
                time.sleep(1)
                self.device(text="收下水滴").click_exists(timeout=1)
                time.sleep(1)
            if not self.device(text="去逛逛").exists:
                break
            self.device(text="去逛逛").click_exists(timeout=1)
            time.sleep(random.randint(8, 10))
            for j in range(3):
                self.back()
                if self.device(text="东东农场").exists:
                    break
            self.device(text="去领取").click_exists(timeout=1)
            time.sleep(1)

    def close_task_page(self):
        """关闭任务页"""
        print('关闭任务页')
        self.device.click(0.954, 0.473)

    def handle_paradise(self):
        """处理京东乐园任务"""
        # 打开京东乐园
        self.open_paradise_page()
        # 处理京东乐园浏览任务
        self.handle_paradise_scan()
        # 抽奖
        self.lucky_draw()
        # 关闭京东乐园任务页
        self.close_paradise_page()

    def handle_collect(self):
        """处理收集任务"""
        # 打开任务页
        self.open_task_page()
        # 处理浏览任务
        self.handle_scan()
        # 关闭任务页
        self.close_task_page()

    def handle_task(self):
        """处理任务"""
        # 处理收集任务
        self.handle_collect()
        # 处理签到
        self.handle_sign()
        # 处理京东乐园任务
        self.handle_paradise()

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
        # 打开京东农场
        self.open_farm()
        # 处理任务
        self.handle_task()
        # 关闭京东
        self.app_stop(MobileControl.APP_JD)
