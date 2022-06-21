#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import time

from package.tools.SystemInput.MouseCommand import MouseCommand
from package.tools.DateType.DateType import DateType


class TimLineWorkTime:
    """打卡"""

    @staticmethod
    def work_time_task(ignore_date_type=False):
        """自动打卡"""
        if not ignore_date_type and not DateType.is_work_day() and 'unknown' != DateType.get_date_type():
            return

        # 关闭当前咚咚进程
        os.system('taskkill /f /im Timline.exe')
        time.sleep(10)
        # 重新打开咚咚
        tim_line = os.popen('Timline', 'r')
        time.sleep(90)

        tim_line_point = (1435, 148)  # 咚咚上最大化按钮的位置
        MouseCommand.left_click(tim_line_point)

        # 确保咚咚处于窗口最大化状态
        MouseCommand.windows_system_command('window_max')
        time.sleep(2)

        work_time_point = (1680, 34)  # 咚咚上打卡按钮的位置
        submit_point = (1400, 630)  # pc页面上打卡按钮的位置
        # 打开打卡页面
        MouseCommand.left_click(work_time_point)
        time.sleep(90)
        # 确保浏览器处于窗口最大化状态
        MouseCommand.windows_system_command('window_max')
        time.sleep(2)
        # 打卡
        MouseCommand.left_click(submit_point)
        time.sleep(2)
        os.system('taskkill /f /im Timline.exe')
        time.sleep(3)
        # 关闭
        tim_line.close()
