#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import time
import _thread

from package.tools.SystemInput.MouseCommand import MouseCommand
from package.tools.DateType.DateType import DateType


class MEWorkTime:
    """打卡"""

    @staticmethod
    def open_me():
        # 关闭当前京ME进程
        os.system('taskkill /f /im ME.exe')
        time.sleep(10)
        # 重新打开咚咚
        os.system("ME >> null")
        time.sleep(40)
        os.system('taskkill /f /im ME.exe')

    @staticmethod
    def time_submit():
        time.sleep(60)

        # 窗口最大化
        MouseCommand.windows_system_command('window_max')
        time.sleep(2)

        # 打开工作台
        work_plant_pos = (37, 473)
        MouseCommand.left_click(work_plant_pos)
        time.sleep(5)
        # 选择首页
        home_page_pos = (133, 67)
        MouseCommand.left_click(home_page_pos)
        time.sleep(5)
        # 选择打卡功能
        work_time_pos = (356, 398)
        MouseCommand.left_click(work_time_pos)
        time.sleep(5)
        # 打卡
        submit_pos = (1400, 561)
        MouseCommand.left_click(submit_pos)
        time.sleep(2)

    @staticmethod
    def work_time_task(ignore_date_type=False):
        """自动打卡"""
        # if not ignore_date_type and not DateType.is_work_day() and 'unknown' != DateType.get_date_type():
        #     return

        print('ccc')
        _thread.start_new_thread(MEWorkTime.open_me, ())
        _thread.start_new_thread(MEWorkTime.time_submit, ())

        time.sleep(100)
