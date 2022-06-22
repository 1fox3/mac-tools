#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import time

from package.config.Env import get_env_config
from package.config.JD import get_jd_config
from package.tools.DateType.DateType import DateType


class BrowserWorkTime:
    """打卡"""

    @staticmethod
    def only_open_page(url):
        """仅打开打卡页面"""
        browser = get_env_config('browser', '')
        browser_resource = os.popen(browser + ' ' + url)
        time.sleep(2)
        browser_resource.close()

    @staticmethod
    def open_work_time_page(url, ignore_date_type=False):
        """自动打卡"""
        # 判断是否为法定工作日
        if not ignore_date_type and not DateType.is_work_day() and 'unknown' != DateType.get_date_type():
            return

        BrowserWorkTime.only_open_page(url)

    @staticmethod
    def open_erp_page(ignore_date_type=False):
        html_dict = get_jd_config('html_list', {})
        if isinstance(html_dict, dict) and 'erp_url' in html_dict.keys():
            BrowserWorkTime.open_work_time_page(html_dict['erp_url'], ignore_date_type)

    @staticmethod
    def open_kaoqin_page(ignore_date_type=False):
        html_dict = get_jd_config('html_list', {})
        if isinstance(html_dict, dict) and 'kaoqin_url' in html_dict.keys():
            BrowserWorkTime.open_work_time_page(html_dict['kaoqin_url'], ignore_date_type)
