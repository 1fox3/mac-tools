#!/usr/bin/env python3
# -*-coding:utf-8 -*-

"""自动打卡"""
import traceback
import time
import random

from package.tools.JD.BrowserWorkTime import BrowserWorkTime
from package.tools.Log.DBLog import DBLog

if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        # 随机延时一段时间
        time.sleep(random.randint(1, 300))
        BrowserWorkTime.open_erp_page()
    except Exception as e:
        DBLog.log(**{
            'break_point': 'browserAutoWorkTimeSubmitException',
            'log_info': traceback.format_exc()
        })
    exit(0)
