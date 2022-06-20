#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from package.tools.Log.DBLog import DBLog


class File:
    """文件相关操作"""
    # 读模式
    readMode = [
        'r',
        'rb',
        'r+',
        'rb+',
        'w+',
        'wb+',
        'a+',
        'ab+',
    ]
    # 写模式
    writeMode = [
        'w'
        'wb'
        'w+'
        'wb+'
        'a'
        'ab'
        'a+',
        'ab+',
    ]

    def __init__(self):
        self.break_point = ''
        self.log_info = {}

    def log_return(self, data):
        """返回"""
        log_param = {
            'break_point': self.break_point,
            'log_info': self.log_info,
        }
        DBLog.log(**log_param)
        return data

    def open(self, file_path, mode='r'):
        """打开文件"""
        self.break_point = 'open_file_failed'
        self.log_info = {
            'file_path': file_path,
        }
        try:
            file_obj = open(file_path, mode, encoding='utf-8')
        except Exception as e:
            self.log_info['exception_msg'] = e
            return self.log_return(None)
        except OSError as e:
            self.log_info['error_msg'] = e
            return self.log_return(None)
        return file_obj
