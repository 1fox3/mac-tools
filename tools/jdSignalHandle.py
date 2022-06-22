#!/usr/bin/env python3
# -*-coding:utf-8 -*-

"""自动打卡"""
import traceback

from package.tools.JD.BrowserWorkTime import BrowserWorkTime
from package.tools.Log.DBLog import DBLog
from package.service.signal.Signal import Signal

if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        signal = Signal()
        ret = signal.get_last_signal('jd')
        if ret and ret.get('id') and ret.get('signal_value') and '' == ret.get('handle_status'):
            signal.start(ret.get('id'))
            handle_status = 'success'
            signal_value = ret.get('signal_value')
            if 'timLineWorkTime' == signal_value:
                BrowserWorkTime.open_kaoqin_page(True)
            elif 'browserWorkTime' == signal_value:
                BrowserWorkTime.open_erp_page(True)
            else:
                handle_status = 'unhandled'
            signal.end(ret.get('id'), handle_status)
    except Exception as e:
        DBLog.log(**{
            'break_point': 'jdSignalHandle',
            'log_info': traceback.format_exc()
        })
