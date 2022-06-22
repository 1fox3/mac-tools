#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import time

from package.model.admin.TSignal import TSignal


class Signal:
    """信号服务类"""

    def __init__(self):
        self.signal_model = TSignal()

    def start(self, signal_id):
        """开始处理"""
        return self.signal_model.update(
            {'id': signal_id},
            {'start_handle_time': time.strftime('%Y-%m-%d %H:%M:%S')}
        )

    def end(self, signal_id, handle_status):
        """开始处理"""
        return self.signal_model.update(
            {'id': signal_id},
            {'end_handle_time': time.strftime('%Y-%m-%d %H:%M:%S'), 'handle_status': handle_status}
        )

    def get_last_signal(self, signal):
        """获取最新的信号"""
        return self.signal_model.get_one({'signal': signal}, {'order by': 'id DESC'})
