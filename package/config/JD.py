#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# 系统环境配置
JD = {
    'erp_info': {
        'erp': 'lusongsong2',
        'password': 'Lss20181122!2',
    },
    'email': 'lusongsong@jd.com',
    # 功能页面地址
    'html_list': {
        # 打卡
        'erp_url': 'http://erp.jd.com/',
        'kaoqin_url': 'http://kaoqin.jd.com/',
    },
}


def get_jd_config(key, default=None):
    """获取配置"""
    if isinstance(key, str):
        key_list = [key]
    if isinstance(key, list):
        key_list = key
    if not key_list:
        return default
    config = JD
    for config_key in key_list:
        config_keys = config.keys()
        if config_keys and config_key in config_keys:
            config = config[config_key]
            continue
        else:
            config = default
            break
    return config
