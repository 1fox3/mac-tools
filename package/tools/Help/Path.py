#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os


class Path:
    """路径相关操作"""

    @staticmethod
    def path_suit_sys(path_str, fill_end=False):
        """将路径中的分割符替换成系统默认分割符"""
        seps = r'\/'
        sep_other = seps.replace(os.sep, '')
        path_str = path_str.replace(sep_other, os.sep) if sep_other in path_str else path_str
        return path_str + os.sep if fill_end and not path_str.endswith(os.sep) else path_str
