#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import time
import re
import random

from package.tools.SystemInput.MouseCommand import MouseCommand
from package.config.JD import get_jd_config
from package.config.Env import get_env_config
from package.tools.Browser.SaveHtml import SaveHtml
from package.tools.DateType.DateType import DateType
from package.tools.JD.BrowserLogin import BrowserLogin


class BrowserWorkTime:
    """打卡"""

    # 页面保存名称
    htmlSaveName = 'workTime'

    def __init__(self):
        self.browser_resource = None
        self.work_time_url = get_jd_config(['html_list', 'work_time'], '')
        self.browser = get_env_config('browser', '')

    def only_open_page(self):
        """仅打开打卡页面"""
        self.browser_resource = os.popen(self.browser + ' ' + self.work_time_url)
        time.sleep(2)
        self.browser_resource.close()

    def open_page(self):
        """打开打卡页面"""
        self.browser_resource = os.popen(self.browser + ' ' + self.work_time_url)
        time.sleep(20)

        # 确保浏览器处于窗口最大化状态
        MouseCommand.windows_system_command('window_max')
        time.sleep(2)

    @staticmethod
    def save_page():
        """保存打卡页面"""
        return SaveHtml.save_page(BrowserWorkTime.htmlSaveName)

    @staticmethod
    def get_work_time_info(html_path):
        """获取订餐列表"""
        work_time_info = {}
        if os.path.exists(html_path) and os.path.isfile(html_path) and \
                os.access(html_path, os.F_OK) and os.access(html_path, os.R_OK):
            html_file = open(html_path, 'r', encoding='utf-8')
            html_content = html_file.readlines()
            pattern = r"<p class=\"(.*?)\">(.*?)</p>"
            for line_str in html_content:
                match = re.search(pattern, line_str)
                if match:
                    info_type = match.group(1)
                    content = match.group(2)
                    if 'check-date' == info_type:
                        date_arr = content.split(' ')
                        work_time_info['date'] = date_arr[0] if date_arr else None
                    if 'check-begin' == info_type:
                        begin_arr = content.split(' ')
                        if '未打卡' != begin_arr[1]:
                            work_time_info['start_time'] = begin_arr[1] if 2 <= len(begin_arr) else None
                    if 'check-long' == info_type:
                        date_arr = content.split(':')
                        work_time_info['work_time'] = date_arr[1] if 2 <= len(date_arr) else None
                    if 'check-time' == info_type:
                        begin_arr = content.split(' ')
                        if '未打卡' != begin_arr[1]:
                            work_time_info['end_time'] = begin_arr[1] if 2 <= len(begin_arr) else None
        return work_time_info

    def console_submit_work_time(self):
        """打卡"""
        # 防止出现中文输入法混乱
        MouseCommand.reset_input_kind()

        # 调起调试工具，并切换到console栏目
        MouseCommand.key_input('F12')
        time.sleep(1)
        MouseCommand.multi_key_input(['ctrl', '2'])
        time.sleep(1)

        # 打卡
        commands = [
            '',
            'checkIn()',
        ]
        for command in commands:
            MouseCommand.input_command(command + '\n')
            time.sleep(1)

        self.browser_resource.close()

    @staticmethod
    def work_time_task(ignore_date_type=False):
        """自动打卡"""
        # 判断是否为法定工作日
        if not ignore_date_type and not DateType.is_work_day() and 'unknown' != DateType.get_date_type():
            return

        work_timer_obj = BrowserWorkTime()
        time_limit = 300
        once_limit = 60
        while True:
            work_timer_obj.open_page()
            html_file_path = work_timer_obj.save_page()
            if html_file_path:
                break
            else:
                time_limit -= once_limit
                time.sleep(once_limit)
            if 0 >= time_limit:
                break
        work_time_info = work_timer_obj.get_work_time_info(html_file_path)
        # 需要登录
        if not work_time_info:
            login_obj = BrowserLogin()
            login_obj.input_erp_password()
        work_timer_obj.console_submit_work_time()

    @staticmethod
    def open_page_work_time_task(ignore_date_type=False):
        """自动打卡"""
        # 判断是否为法定工作日
        if not ignore_date_type and not DateType.is_work_day() and 'unknown' != DateType.get_date_type():
            return

        work_timer_obj = BrowserWorkTime()
        work_timer_obj.only_open_page()
