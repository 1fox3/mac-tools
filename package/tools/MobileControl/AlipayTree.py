#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import time

from package.tools.MobileControl.MobileControl import MobileControl


class AlipayTree(MobileControl):
    """支付宝芭芭农场"""

    def open_tree(self, delay=10):
        """通过助力的方式打开芭芭农场"""
        print("打开芭芭农场")
        self.device(text="消息").click_exists(timeout=2)
        time.sleep(5)
        self.device(text="玉洁").click_exists(timeout=2)
        time.sleep(5)
        self.device(text="帮我助力，你也有奖励").click_exists(timeout=2)
        time.sleep(5)
        self.device(text="为Ta助力").click_exists(timeout=2)
        time.sleep(5)
        self.device(text="去种果树").click_exists(timeout=2)
        time.sleep(delay)

    def collect_fertilizer(self, delay=2):
        """领取肥料"""
        print('领取肥料')
        self.device.click(0.803, 0.62)
        time.sleep(1)
        self.device.click(0.496, 0.715)
        time.sleep(delay)

    def open_collect_fertilizer_page(self, delay=1):
        """打开领肥料页面"""
        self.device.click(0.883, 0.817)
        time.sleep(delay)

    def close_collect_fertilizer_page(self, delay=1):
        """关闭领肥料页面"""
        self.device.click(0.923, 0.316)
        time.sleep(delay)

    def collect(self):
        """领取奖励"""
        self.device(text='领取').click_exists(timeout=2)

    def alipay_farm_fertilizer(self, delay=1):
        """领取蚂蚁庄园肥料"""
        if self.device(text="领取", clickable=True).exists:
            for elem in self.device.xpath("//*[@text='领取']").all():
                elem.click()
                time.sleep(2)
            time.sleep(delay)

    def scan_story(self, delay=2):
        """浏览故事"""
        print("浏览故事")
        self.device(text="去看看").click_exists(timeout=2)
        time.sleep(delay)
        if self.device(text="去看看", index=1).exists:
            self.device(text="去看看", index=1).click_exists(timeout=2)
            time.sleep(delay)
            self.back()
            self.collect()

    def get_goods_pos(self):
        """查找浏览商品位置"""
        print('查找浏览商品位置')
        for i in range(4):
            goods_str = ' 逛一逛领1500肥料 (' + str(i) + '/3)'
            if self.device(text=goods_str).exists:
                return [i, self.device(text=goods_str).bounds()]
        return None

    def scan_goods(self, delay=2):
        """浏览商品"""
        print("浏览商品")
        shop_pos = self.get_goods_pos()
        if shop_pos is None or 3 == shop_pos[0]:
            return
        for elem in self.device.xpath("//*[@text='去完成']").all():
            if elem.bounds[1] > shop_pos[1][1]:
                for i in range(3 - shop_pos[0]):
                    elem.click()
                    time.sleep(7)
                    self.device.swipe(500, 950, 500, 800)
                    time.sleep(18)
                    self.back()
                    time.sleep(2)
                break
        time.sleep(delay)

    def goto_taobao(self, delay=50):
        """去淘宝"""
        print('去淘宝')
        for i in range(2):
            # 滑动任务列表
            self.device.swipe(500, 1515, 500, 654)
            if not self.device(text="逛淘宝芭芭农场领900肥料").exists:
                continue
            if self.device(text="去逛逛").exists and self.device(text=" 逛逛淘宝芭芭农场 (0/1)").exists:
                goto_taobao_pos = self.device(text=" 逛逛淘宝芭芭农场 (0/1)").bounds()
                for elem in self.device.xpath("//*[@text='去逛逛']").all():
                    if elem.bounds[1] > goto_taobao_pos[1]:
                        elem.click()
                        time.sleep(delay)
                        self.app_stop(MobileControl.APP_TAOBAO)
                        for j in range(3):
                            if not self.device(text="逛淘宝芭芭农场领900肥料").exists:
                                self.back()

    def handle_collect_fertilizer_task(self):
        """处理领肥料任务"""
        # 领取肥料
        self.collect_fertilizer()
        # 打开领肥料页面
        self.open_collect_fertilizer_page()
        # 领取蚂蚁庄园肥料
        self.alipay_farm_fertilizer()
        # 浏览故事
        # self.scan_story()
        # 浏览商品
        self.scan_goods()
        # 去淘宝
        self.goto_taobao()
        # 关闭领肥料页面
        self.close_collect_fertilizer_page()
        # 领取肥料
        self.collect_fertilizer()

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
        # 打开芭芭农场
        self.open_tree()
        # 处理领肥料任务
        self.handle_collect_fertilizer_task()
        # 关闭支付宝
        self.app_stop(MobileControl.APP_ALIPAY)
