#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# 系统环境配置
Env = {
    # ssh配置
    'ssh': 'Noah',
    'ssh_config': {
        'Noah': {
            'run_name': 'open -a Terminal .',
            'log_path': '/Users/lusongsong/Logs',
            'log_format': '%Y-%m-%d',
            'download_path': '/Users/lusongsong/Downloads',
            'url': 'bastion.jd.com',
        },
    },
    # 默认浏览器启动路径
    'browser': 'open /Applications/Google\ Chrome.app',
    'php': '/Applications/XAMPP/xamppfiles/bin/php-7.4.29',
    # 默认服务
    'main_service': 'GE',
}


def get_env_config(key, default=None):
    """获取配置"""
    if isinstance(key, str):
        key_list = [key]
    if isinstance(key, list):
        key_list = key
    if not key_list:
        return default
    config = Env
    for config_key in key_list:
        config_keys = config.keys()
        if config_keys and config_key in config_keys:
            config = config[config_key]
            continue
        else:
            config = default
            break
    return config
