#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import time

from package.tools.MobileControl.MobileControl import MobileControl


class TaoBaoTree(MobileControl):
    """淘宝芭芭农场种树"""

    def help(self, delay=20):
        """助力"""
        print('助力')
        self.device.xpath('//*[@content-desc="消息"]/android.widget.ImageView[1]').click_exists(timeout=2)
        time.sleep(10)
        self.device(description="张玉洁").click_exists(timeout=2)
        time.sleep(5)
        # 通过消息体的位置确定发送人
        comm_x = 0
        message_list = self.device.xpath("//*[@resource-id='com.taobao.taobao:id/tv_chatcontent']").all()
        pos = 0
        for i in range(len(message_list)):
            elem = message_list[i]
            if 0 == i:
                comm_x = elem.bounds[0]
                continue
            else:
                pos = i if elem.bounds[0] < comm_x else i - 1
                break
        message_list[pos].click()
        time.sleep(5)
        self.device(text="为TA助力").click_exists(timeout=2)
        time.sleep(5)
        self.device(text="去种果树").click_exists(timeout=2)
        time.sleep(delay)

    def collect_fertilizer(self, delay=2):
        """领取肥料"""
        print('领取肥料')
        self.device.click(0.8, 0.63)
        time.sleep(delay)
        self.device(text="关闭").click_exists(timeout=2)
        # self.device.click(0.498, 0.744)

    def open_collect_fertilizer_page(self, delay=1):
        """打开领肥料页面"""
        print('打开领肥料页面')
        self.device.click(0.784, 0.841)
        time.sleep(delay)

    def sign_in(self, delay=1):
        """签到"""
        print('签到')
        if self.device(text="去签到").exists:
            self.device(text="去签到").click_exists(timeout=2)
            time.sleep(delay)

    def collect(self):
        """领取奖励"""
        self.device(text='领取').click_exists(timeout=2)

    def scan_goods(self, delay=2):
        """浏览商品"""
        print("浏览商品")
        for i in range(5):
            if self.device(text="去逛逛", index=1).exists:
                self.device(text="去逛逛", index=1).click_exists(timeout=2)
                time.sleep(7)
                # 掷骰子
                if self.device(text="本地图奖励服装").exists:
                    self.device.click(0.482, 0.609)
                    time.sleep(3)
                self.device.swipe(500, 950, 500, 800)
                time.sleep(18)
                for j in range(3):
                    if not self.device(text="已完成").exists:
                        self.back()
                time.sleep(delay)

    def collect_gift(self, delay=2):
        """领取礼包"""
        print("领取礼包")
        if self.device(text="去领取").exists:
            self.device(text="去领取").click_exists(timeout=2)
            time.sleep(delay)

    def goto_alipay(self, delay=50):
        """去支付宝"""
        print("去支付宝")
        if self.device(text="去逛逛").exists and self.device(text="逛逛支付宝芭芭农场(0/1)").exists:
            goto_alipay_pos = self.device(text="逛逛支付宝芭芭农场(0/1)").bounds()
            for elem in self.device.xpath("//*[@text='去逛逛']").all():
                if elem.bounds[1] > goto_alipay_pos[1]:
                    elem.click()
                    time.sleep(delay)
                    self.app_stop(MobileControl.APP_ALIPAY)

    def scan_task(self, delay=2):
        """浏览任务"""
        print("浏览任务")
        for i in range(4):
            if self.device(text="逛逛'买多少返多少'(0/1)").exists:
                self.device(text="逛逛'买多少返多少'(0/1)").click()
                time.sleep(3)
                self.device.click(0.922, 0.266)
                time.sleep(7)
                self.device.swipe(500, 950, 500, 800)
                time.sleep(18)
                self.back()
                continue
            if self.device(text="浏览15秒得300肥料").exists:
                self.device(text="浏览15秒得300肥料").click()
                time.sleep(7)
                self.device.swipe(500, 950, 500, 800)
                time.sleep(18)
                self.back()
            else:
                break
        time.sleep(delay)

    def handle_farm_task(self):
        """处理农场任务"""
        # 领取肥料
        self.collect_fertilizer()
        # 领取兔子挖到的肥料
        self.device.click(0.192, 0.637)
        # 帮助好友施肥
        # self.help_friend_fertilizer()
        # 打开领饲料页面
        self.open_collect_fertilizer_page()
        # 签到
        self.sign_in()
        # 答题
        self.answer()
        # 滑动任务列表
        self.device.swipe(500, 1515, 500, 804)
        # 领取礼包
        self.collect_gift()
        # 浏览任务
        self.scan_task()
        # 浏览商品
        self.scan_goods()
        # 去支付宝
        self.goto_alipay()

    def help_friend_fertilizer(self, delay=2):
        """帮助好友施肥"""
        print("帮助好友施肥")
        self.device.click(0.242, 0.839)
        time.sleep(4)
        if self.device(text="张玉洁").exists:
            self.device.click(0.824, 0.47)
            time.sleep(2)
            self.device.click(0.824, 0.47)
            time.sleep(2)
        self.back()
        time.sleep(delay)

    def answer(self, delay=3):
        """答题"""
        print("答题")
        if self.device(text="农场百科问答(0/1)").exists:
            self.device(text="农场百科问答(0/1)").click()
            time.sleep(3)
            # 选择答案1
            # self.device.click(0.482, 0.823)
            # 选择答案2
            self.device.click(0.501, 0.888)
            time.sleep(3)
            # for i in range(1, 11):
            #     text = '领取（' + str(i * 50) + '肥料）'
            #     if self.device(text=text).exists:
            #         self.device(text=text).click_exists(timeout=2)
            #         break
            # 领肥料
            self.device.click(0.501, 0.888)
            time.sleep(delay)
            # 打开领饲料页面
            self.open_collect_fertilizer_page()

    def start_task(self, ip):
        """开始执行任务"""
        # 链接手机
        self.connect(ip)
        # 回到主页面
        self.home()
        # 关闭淘宝
        self.app_stop(MobileControl.APP_TAOBAO)
        # 打开淘宝
        self.app_start(MobileControl.APP_TAOBAO)
        # 打开芭芭农场
        self.help()
        # 处理农场任务
        self.handle_farm_task()
        # 关闭支付宝
        self.app_stop(MobileControl.APP_TAOBAO)
