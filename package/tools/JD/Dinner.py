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
from package.model.mba.TWorkDinner import TWorkDinner
from package.tools.JD.BrowserLogin import BrowserLogin


class Dinner:
    """加班餐"""

    # 页面保存名称
    htmlSaveName = 'dinner'
    dinnerSplitStr = ['-', '—']

    def __init__(self):
        self.browser_resource = None
        self.dinner_url = get_jd_config(['html_list', 'dinner'], '')
        self.browser = get_env_config('browser', '')

    def open_dinner_page(self):
        """打开订餐页面"""
        # 打开订餐页面
        os.popen(self.browser + ' ' + self.dinner_url)

    def open_page(self):
        """打开订餐页面"""
        # 打开订餐页面
        self.browser_resource = os.popen(self.browser + ' ' + self.dinner_url)
        time.sleep(20)

        # 确保浏览器处于窗口最大化状态
        MouseCommand.windows_system_command('window_max')
        time.sleep(2)

        # 进行登录操作
        # login_point = (950, 580)  # 登录的位置
        # MouseCommand.left_click(login_point)
        # time.sleep(1)

        # 已启用Chrome自动登录插件，无需再登录
        # login_obj = BrowserLogin()
        # login_obj.input_erp_password()
        # time.sleep(5)

    @staticmethod
    def save_page():
        """保存订餐页面"""
        return SaveHtml.save_page(Dinner.htmlSaveName)

    @staticmethod
    def get_dinner_list(html_path):
        """获取订餐列表"""
        dinner_list = {}
        if os.path.exists(html_path) and os.path.isfile(html_path) and \
                os.access(html_path, os.F_OK) and os.access(html_path, os.R_OK):
            html_file = open(html_path, 'r', encoding='utf-8')
            html_content = html_file.readlines()
            pattern = r"name=\"optionsRadios\" id=\"dinner_([\d]+)\" value=\"(.*?)\""
            for line_str in html_content:
                match = re.search(pattern, line_str)
                if match:
                    dinner_id = match.group(1)
                    dinner = match.group(2)
                    dinner_arr = []
                    for splitStr in Dinner.dinnerSplitStr:
                        if -1 != dinner.find(splitStr):
                            dinner_arr = dinner.split(splitStr)
                    if not dinner_arr:
                        continue
                    # 数据表中加班餐类型是枚举类型，所以必须重置成枚举类型中的某项
                    dinner_type = dinner_arr[1]
                    if dinner_type.startswith('东家小院'):
                        dinner_type = '东家小院'
                    else:
                        dinner_type = '天象'
                    dinner_list[dinner_arr[0]] = {
                        'id': dinner_id,
                        'dinner_type': dinner_type,
                        'dinner_name': dinner_arr[0],
                    }
        return dinner_list

    @staticmethod
    def choose_dinner(dinner_list):
        """选择加班餐"""
        # 查找已经设置的可选餐
        support_dinner_list = {}
        model_obj = TWorkDinner()
        for dinner in dinner_list.values():
            dinner = dict(dinner)
            if 'id' in dinner.keys():
                dinner_id = dinner.pop('id')
            dinner_info = model_obj.get_one(dinner)
            if dinner_info:
                if 0 != dinner_info['weight']:
                    dinner_info['id'] = dinner_id
                    support_dinner_list[dinner_id] = dinner_info
            else:
                model_obj.insert(dinner)
        dinner_list_keys = list(dinner_list.keys())
        if not support_dinner_list:
            # 全部都无设置，则默认从前3个中随机一个
            dinner_id = random.randint(1, 3)
            dinner_info = dinner_list[dinner_list_keys[dinner_id]]
        else:
            # 根据权重随机选一个
            max_int = 0
            for support_dinner in support_dinner_list.values():
                max_int += int(support_dinner['weight'])
            random_dinner_weight = random.randint(1, max_int)
            for support_dinner in support_dinner_list.values():
                random_dinner_weight -= int(support_dinner['weight'])
                if random_dinner_weight <= 0:
                    dinner_info = support_dinner
                    break
        return dinner_info

    def console_submit_dinner(self, dinner_info):
        """确定加班餐"""
        # 防止出现中文输入法混乱
        MouseCommand.reset_input_kind()
        # 调起调试工具，并切换到console栏目
        MouseCommand.key_input('F12')
        time.sleep(1)
        MouseCommand.multi_key_input(['ctrl', '2'])
        time.sleep(1)

        # 执行选餐和确定过程
        dinner_id = 'uniform-dinner_' + dinner_info['id']
        submit_id = 'save_dinner'
        commands = [
            '',
            '$(\'#' + dinner_id + '\').click()',
            '$(\'#' + submit_id + '\').click()',
        ]
        for command in commands:
            MouseCommand.input_command(command + '\n')
            time.sleep(1)

        self.browser_resource.close()

    def mouse_click_submit_dinner(self, dinner_info):
        """通过鼠标点击订餐"""
        dinner_list_x = 565
        dinner_list_y = 307 + 32 * int(dinner_info['id'])
        dinner_point = (dinner_list_x, dinner_list_y)  # 小院中餐的位置
        submit_point = (575, 810)  # 提交的位置
        points = [dinner_point, submit_point]  # 需要点击的点数组
        for point in points:
            MouseCommand.left_click(point)
            time.sleep(1)
        self.browser_resource.close()

    @staticmethod
    def dinner_task(ignore_date_type=False):
        """自动定加班餐"""
        # 判断是否为法定工作日
        if not ignore_date_type and not DateType.is_work_day() and 'unknown' != DateType.get_date_type():
            exit(0)
        dinner_obj = Dinner()
        dinner_obj.open_dinner_page()

        # dinner_obj = Dinner()
        # time_limit = 300
        # once_limit = 60
        # while True:
        #     dinner_obj.open_page()
        #     html_file_path = dinner_obj.save_page()
        #     if html_file_path:
        #         break
        #     else:
        #         time_limit -= once_limit
        #         time.sleep(once_limit)
        #     if 0 >= time_limit:
        #         break
        # dinner_list = Dinner.get_dinner_list(html_file_path)
        # dinner_info = Dinner.choose_dinner(dinner_list)
        # dinner_obj.console_submit_dinner(dinner_info)
