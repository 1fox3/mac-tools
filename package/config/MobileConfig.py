#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
手机控制相关配置
"""
AppPackage = {
    # 支付宝
    'Alipay': 'com.eg.android.AlipayGphone',
    'Taobao': 'com.taobao.taobao',
    'JD': 'com.jingdong.app.mall',
}


def app_package(app):
    """获取app的包名以便于打开对应的APP"""
    if app in AppPackage.keys():
        return AppPackage[app]
    return ''
