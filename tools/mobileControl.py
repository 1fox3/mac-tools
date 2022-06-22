#!/usr/bin/env python3
# -*-coding:utf-8 -*-

import uiautomator2 as u2
import time
import datetime

from package.tools.MobileControl.AlipayTree import AlipayTree
from package.tools.MobileControl.AlipayForest import AlipayForest
from package.tools.MobileControl.AlipayFarm import AlipayFarm
from package.tools.MobileControl.TaoBaoFarm import TaoBaoFarm
from package.tools.MobileControl.TaoBaoTree import TaoBaoTree
from package.tools.MobileControl.JDBean import JDBean
from package.tools.MobileControl.JDBeanField import JDBeanField
from package.tools.MobileControl.JDFarm import JDFarm
from package.tools.MobileControl.JDShopUnsubscribe import JDShopUnsubscribe
from package.tools.MobileControl.JDGoodsUnsubscribe import JDGoodsUnsubscribe
from package.tools.MobileControl.JDScanLogClear import JDScanLogClear


def alipay_forest(ip):
    """支付宝蚂庄森林"""
    try:
        alipay_forest_obj = AlipayForest()
        alipay_forest_obj.start_task(ip)
    except Exception as e:
        print(e)


def alipay_tree(ip):
    """支付宝芭芭农场"""
    try:
        alipay_tree_obj = AlipayTree()
        alipay_tree_obj.start_task(ip)
    except Exception as e:
        print(e)


def alipay_farm(ip):
    """支付宝蚂蚁庄园"""
    try:
        alipay_farm_obj = AlipayFarm()
        alipay_farm_obj.start_task(ip)
    except Exception as e:
        print(e)


def taobao_farm(ip):
    """淘宝芭芭农场"""
    try:
        taobao_farm_obj = TaoBaoFarm()
        taobao_farm_obj.start_task(ip)
    except Exception as e:
        print(e)


def taobao_tree(ip):
    """淘宝芭芭农场种树"""
    try:
        taobao_tree_obj = TaoBaoTree()
        taobao_tree_obj.start_task(ip)
    except Exception as e:
        print(e)


def jd_bean(ip):
    """京东领京豆"""
    try:
        jd_bean_obj = JDBean()
        jd_bean_obj.start_task(ip)
    except Exception as e:
        print(e)


def jd_bean_field(ip):
    """京东种豆得豆"""
    try:
        jd_bean_field_obj = JDBeanField()
        jd_bean_field_obj.start_task(ip)
    except Exception as e:
        print(e)


def jd_farm(ip):
    """京东农场"""
    try:
        jd_farm_obj = JDFarm()
        jd_farm_obj.start_task(ip)
    except Exception as e:
        print(e)


def jd_shop_unsubscribe(ip):
    """京东店铺取消关注"""
    try:
        jd_shop_unsubscribe_obj = JDShopUnsubscribe()
        jd_shop_unsubscribe_obj.start_task(ip)
    except Exception as e:
        print(e)


def jd_goods_unsubscribe(ip):
    """京东商品取消收藏"""
    try:
        jd_goods_unsubscribe_obj = JDGoodsUnsubscribe()
        jd_goods_unsubscribe_obj.start_task(ip)
    except Exception as e:
        print(e)


def jd_scan_log_clear(ip):
    """京东清除浏览记录"""
    try:
        jd_scan_log_clear_obj = JDScanLogClear()
        jd_scan_log_clear_obj.start_task(ip)
    except Exception as e:
        print(e)


def jd_clear(ip):
    """京东清除数据"""
    # 京东店铺取消关注
    jd_shop_unsubscribe(ip)
    # 京东商品取消收藏
    jd_goods_unsubscribe(ip)
    # 京东清除浏览记录
    jd_scan_log_clear(ip)


def mobile_task(ip):
    """手机任务"""
    # 支付宝蚂蚁森林(能量雨)
    alipay_forest(ip)
    # 支付宝芭芭农场
    alipay_tree(ip)
    # 支付宝蚂蚁庄园(赶小鸡，收饲料)
    # alipay_farm(ip)
    # 淘宝芭芭农场(商品推荐页面关闭)
    taobao_farm(ip)
    # 淘宝芭芭农场种树
    taobao_tree(ip)
    # 京东领京豆
    jd_bean(ip)
    # 京东种豆得豆
    jd_bean_field(ip)
    # 京东农场
    jd_farm(ip)
    # 京东清理关注记录(周一)
    if 0 == datetime.datetime.today().weekday():
        jd_clear(ip)


def test_func(ip):
    d = u2.connect(ip)
    for i in range(50):
        for task_str in ["去浏览", "去搜索", "去逛逛", "去完成"]:
            if d(text=task_str).exists:
                d(text=task_str).click()
                break
        time.sleep(25)
        d.press('back')
        time.sleep(5)


def click_func(ip):
    d = u2.connect(ip)
    for i in range(20):
        # d.click(0.794, 0.554)
        d.click(0.677, 0.648)
        # d.click(0.688, 0.739)
        # d.click(0.674, 0.829)
        time.sleep(15)
        d.press('back')
        time.sleep(2)


def short_click_func(ip):
    d = u2.connect(ip)
    for i in range(19):
        d.click(0.486, 0.697)
        time.sleep(4)


def scan_shop(ip):
    d = u2.connect(ip)
    for i in range(13):
        d.click(300, 400)
        time.sleep(20)
        d.press('back')
        time.sleep(5)
    d.press('back')


def scan(ip):
    d = u2.connect(ip)
    for i in range(30):
        d(text="逛一逛").click()
        time.sleep(15)
        d.press('back')
        time.sleep(5)
        d(text="开心收下").click()
        time.sleep(3)


def pdd_js(ip):
    """拼多多浇水"""
    d = u2.connect(ip)
    for i in range(300):
        d.click(0.885, 0.823)
        time.sleep(3)


if __name__ == "__main__":
    mobile_ip = "10.252.109.5"
    # mobile_ip = "192.168.1.7"
    # mobile_ip = ""
    # scan_shop(mobile_ip)
    # test_func(mobile_ip)
    # short_click_func(mobile_ip)
    # click_func(mobile_ip)
    # scan(mobile_ip)
    # pdd_js(mobile_ip)
    # d = u2.connect(mobile_ip)
    # d = u2.connect()
    # exit()

    for i in range(3):
        mobile_task(mobile_ip)
