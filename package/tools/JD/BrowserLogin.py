#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import time
import re
from urllib.parse import *

from package.tools.SystemInput.MouseCommand import MouseCommand
from package.config.JD import get_jd_config
from package.config.Env import get_env_config


class BrowserLogin:
    """登录"""

    # 页面保存名称
    htmlSaveName = 'workTime'

    def __init__(self):
        self.browser_resource = None
        self.login_url = get_jd_config(['html_list', 'login'], '')
        self.erp = get_jd_config(['erp_info', 'erp'], '')
        self.password = get_jd_config(['erp_info', 'password'], '')
        self.browser = get_env_config('browser', '')

    def open_page(self, url):
        """打开打卡页面"""
        self.browser_resource = os.popen(self.browser + ' ' + self.login_url + quote(url))
        time.sleep(5)
        # 防止出现中文输入法混乱
        MouseCommand.reset_input_kind()
        # 确保浏览器处于窗口最大化状态
        MouseCommand.windows_system_command('window_max')
        time.sleep(2)

    def input_erp_password(self):
        """输入账号秘密"""
        # 防止出现中文输入法混乱
        MouseCommand.reset_input_kind()
        MouseCommand.key_input('tab')
        time.sleep(1)
        MouseCommand.input_command(self.erp)
        time.sleep(1)
        MouseCommand.key_input('tab')
        time.sleep(1)
        MouseCommand.input_command(self.password)
        time.sleep(1)
        MouseCommand.key_input('enter')

    def login(self, url):
        """登录网址"""
        self.open_page(url)
        self.input_erp_password()
