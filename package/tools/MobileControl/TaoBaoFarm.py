#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import time

from package.tools.MobileControl.MobileControl import MobileControl


class TaoBaoFarm(MobileControl):
    """淘宝芭芭农场"""
    FarmPos = [
        {'x': 560, 'y': 1470},
        {'x': 358, 'y': 1456},
        {'x': 555, 'y': 1240},
        {'x': 360, 'y': 1145},
        {'x': 755, 'y': 1125},
        {'x': 555, 'y': 1010},
        {'x': 350, 'y': 900},
        {'x': 755, 'y': 900},
        {'x': 555, 'y': 755},
    ]
    SunPos = [
        {'x': 169, 'y': 879},
        {'x': 360, 'y': 756},
        {'x': 572, 'y': 817},
        {'x': 575, 'y': 637},
        {'x': 789, 'y': 752},
        {'x': 954, 'y': 881},
        {'x': 455, 'y': 986},
        {'x': 726, 'y': 999},
    ]

    def open_farm(self, delay=5):
        """打开芭芭农场"""
        print("打开芭芭农场")
        self.device(text="芭芭农场").click()
        time.sleep(8)
        self.device.click(0.893, 0.514)
        time.sleep(delay)

    def close_notice_page(self, delay=1):
        """关闭提示页"""
        print("关闭提示页")
        self.device\
            .xpath('//*[@resource-id="UIBox"]/android.view.View[1]/android.view.View[1]/android.widget.Button[1]/android.view.View[1]') \
            .click_exists(timeout=2)
        time.sleep(delay)

    def collect_fruit(self, delay=2):
        """收集果实"""
        print("收集果实")
        for pos in TaoBaoFarm.FarmPos:
            ori_level = self.get_level()
            self.device.click(**pos)
            time.sleep(1)
            desc_level = self.get_level()
            print(ori_level)
            print(desc_level)
            if desc_level != ori_level:
                time.sleep(4)
                # 关闭升级提示页
                self.device.click(551, 1593)
                time.sleep(2)
                # 关闭作物升级提示
                self.device.click(537, 1372)
                time.sleep(2)
                self.device(text="种下").click_exists(timeout=2)
                time.sleep(2)
        time.sleep(delay)

    def get_level(self):
        """获取等级"""
        level_str = None
        for i in range(4):
            for elem in self.device.xpath('//android.view.View').all():
                if 396 == elem.bounds[0] and 146 == elem.bounds[1] and 500 == elem.bounds[2] and 206 == elem.bounds[3]:
                    level_str = elem.text
                    break
            if level_str is not None:
                break
        return level_str

    def collect_sun(self, delay=2):
        """收集阳光"""
        print("收集阳光")
        for i in range(2):
            for pos in TaoBaoFarm.SunPos:
                self.device.click(**pos)
                time.sleep(0.2)
        time.sleep(delay)
    
    def open_collect_sun_page(self, delay=0.5):
        """打开收集阳光任务页面"""
        print('打开收集阳光任务页面')
        self.device.click(960, 1725)
        time.sleep(delay)

    def scan_goods(self, delay=2):
        """浏览商品"""
        print("浏览商品")
        if self.device(text="后开始任务").exists:
            return
        if self.device(text="去浏览").exists:
            self.device(text="去浏览").click_exists(timeout=3)
            time.sleep(23)
            self.back()
            time.sleep(delay)

    def close_collect_sun_page(self, delay=1):
        """关闭收集阳光任务页面"""
        print('关闭收集阳光任务页面')
        self.device.xpath('//*[@resource-id="app"]/android.view.View[4]/android.view.View[1]')\
            .click_exists(timeout=3)
        time.sleep(delay)

    def open_shop_page(self, delay=4):
        """打开商店页面"""
        print('打开商店页面')
        self.device.click(600, 1728)
        time.sleep(delay)

    def close_shop_page(self, delay=1):
        """关闭商店页面"""
        print('关闭商店页面')
        self.device\
            .xpath('//*[@resource-id="UIBox"]/android.view.View[1]/android.view.View[1]/android.widget.Button[1]')\
            .click_exists(timeout=3)
        time.sleep(delay)

    def buy_accelerator(self, delay=1):
        """购买加速剂"""
        print('购买加速剂')
        if self.device(text='10购买').exists:
            self.device(text='10购买').click_exists(timeout=3)
            self.device(text='确定').click_exists(timeout=3)
            time.sleep(delay)

    def use_accelerator(self, delay=2):
        """使用加速剂"""
        print('使用加速剂')
        if self.device(text='立即使用').exists:
            self.device(text='立即使用').click_exists(timeout=3)
            self.device(text='确定使用').click_exists(timeout=3)
            time.sleep(delay)

    def handle_farm_task(self):
        """处理农场任务"""
        # 如果没有到达农场页面直接返回
        if not self.device(text="等级").exists:
            return
        # 关闭提示页
        self.close_notice_page()
        # 收集果实
        self.collect_fruit()
        # 收集阳光
        self.collect_sun()
        # 打开收集阳光任务页面
        self.open_collect_sun_page()
        # 浏览商品
        self.scan_goods()
        # 关闭收集阳光任务页面
        self.close_collect_sun_page()
        # 收集阳光
        self.collect_sun()
        # 打开商店页面
        self.open_shop_page()
        # 购买加速剂
        self.buy_accelerator()
        # 使用加速剂
        self.use_accelerator()
        # 关闭商店页面
        self.close_shop_page()

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
        self.open_farm()
        # 处理农场任务
        self.handle_farm_task()
        # 关闭支付宝
        self.app_stop(MobileControl.APP_TAOBAO)
