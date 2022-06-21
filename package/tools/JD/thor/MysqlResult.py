#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import time

from package.config.Env import get_env_config
from package.tools.SSH.SSH import SSH
from package.tools.SystemInput.MouseCommand import MouseCommand


class MysqlResult:
    """雷神监控mysql结果集监控"""
    # 添加监控链接
    createUrl = 'http://thor.jd.com/#/manage/access/mysql-result?app_type=3'
    # 更新监控链接
    updateUrl = 'http://thor.jd.com/#/manage/system/update-cfg-result-mysql/'
    # 时间粒度序号
    timeSpaceOrder = {
        '1min': 0,
        '5min': 1,
        'hour': 2,
        'day': 3,
    }
    # 默认时间粒度为1分钟
    defaultTimeSpace = '1min'
    # 默认展示延时为60秒
    defaultShowDelayTime = '60'
    # 默认展示单位
    defaultUnit = '毫秒'
    # 默认数据库host
    defaultMonitorHost = 'gateht3b.jed.jddb.com'
    # 默认数据库db
    defaultMonitorDB = 'ge_log'
    # 默认数据库端口
    defaultMonitorPort = '3358'
    # 默认数据库账号序号
    defaultMonitorUser = 1
    # 默认监控sql
    defaultMonitorSql = 'select 0;'
    # 默认监控sql名
    defaultMonitorName = '空'
    # 小数精度
    defaultDecimalPrecision = 1

    def __init__(self, monitor_info={}):
        """构造函数"""
        # 监控key
        self.monitor_key = None
        # 监控名称
        self.monitor_name = None
        # 监控粒度
        self.time_space = None
        # 抽取时间
        self.query_time = None
        # 展示延时
        self.show_delay_time = None
        # 展示单位
        self.unit = None
        # 第一个监控的数据库host
        self.first_monitor_host = None
        # 第一个监控的数据库db
        self.first_monitor_db = None
        # 第一个监控的数据库端口
        self.first_monitor_port = None
        # 第一个监控的数据库账号
        self.first_monitor_user = None
        # 第一个监控的sql
        self.first_monitor_sql = None
        # 第一个监控的名称
        self.first_monitor_name = None
        # 第二个监控的数据库host
        self.second_monitor_host = None
        # 第二个监控的数据库db
        self.second_monitor_db = None
        # 第二个监控的数据库端口
        self.second_monitor_port = None
        # 第二个监控的数据库账号
        self.second_monitor_user = None
        # 第二个监控的sql
        self.second_monitor_sql = None
        # 第二个监控的名称
        self.second_monitor_name = None
        # 小数精度
        self.decimal_precision = None
        # 浏览器资源
        self.browser_resource = None
        # 根据监控信息设置监控
        self.init_monitor(monitor_info)

    def init_monitor(self, monitor_info={}):
        """加载监控信息"""
        if monitor_info and isinstance(monitor_info, dict):
            monitor_info_keys = monitor_info.keys()
            for monitor_info_key in monitor_info_keys:
                setattr(self, monitor_info_key, str(monitor_info.get(monitor_info_key)))

    def open_browser(self, url):
        """打开浏览器"""
        self.browser_resource = os.popen(get_env_config('browser', '') + ' ' + url)
        # 休眠一段时间，等待页面加载完成
        time.sleep(10)
        # 确保浏览器处于窗口最大化状态
        MouseCommand.windows_system_command('window_max')
        time.sleep(2)

    def close_browser_resource(self):
        """关闭浏览器资源"""
        if self.browser_resource:
            self.browser_resource.close()

    @staticmethod
    def input_content(content):
        """文本框输入"""
        SSH.input_command(content, 1, '')

    @staticmethod
    def is_not_empty_str(content):
        """判断是够为空字符串"""
        return True if isinstance(content, str) and len(content) > 0 else False

    @staticmethod
    def input_if_not_empty(content):
        """内容不为空时输入内容"""
        if MysqlResult.is_not_empty_str(content):
            MouseCommand.multi_key_input(['ctrl', 'a'])
            MysqlResult.input_content(content)

    def create_monitor(self):
        """添加监控"""
        # 打开浏览器
        self.open_browser(MysqlResult.createUrl)

        # 切换到监控key的输入框
        for i in range(14):
            MouseCommand.key_input('tab')

        # 输入监控key
        MysqlResult.input_content(self.monitor_key if self.monitor_key else '')

        # 切换到监控名称的输入框
        MouseCommand.key_input('tab')

        # 输入监控名称
        MysqlResult.input_content(self.monitor_name if self.monitor_name else '')

        # 切换到时间粒度选择框
        MouseCommand.key_input('tab')

        # 选择时间粒度
        monitor_time_space = self.time_space\
            if self.time_space and self.time_space in MysqlResult.timeSpaceOrder.keys()\
            else MysqlResult.defaultTimeSpace
        monitor_time_space_order = MysqlResult.timeSpaceOrder.get(monitor_time_space)
        for i in range(monitor_time_space_order):
            MouseCommand.key_input('right_arrow')

        # 切换到抽取时间输入框
        MouseCommand.key_input('tab')

        # 输入抽取时间
        if self.query_time:
            MysqlResult.input_content(self.query_time)

        # 切换到展示延时输入框
        MouseCommand.key_input('tab')

        # 输入展示延时
        MysqlResult.input_content(self.show_delay_time if self.show_delay_time else MysqlResult.defaultShowDelayTime)

        # 切换到展示单位输入框
        MouseCommand.key_input('tab')

        # 输入单位
        MysqlResult.input_content(self.unit if self.unit else MysqlResult.defaultUnit)

        # 切换到数据第1个sql的数据库地址输入框
        MouseCommand.key_input('tab')

        # 输入数据第1个sql的数据库地址
        MysqlResult.input_content(self.first_monitor_host if self.first_monitor_host
                                  else MysqlResult.defaultMonitorHost)

        # 切换到数据第1个sql的数据库输入框
        MouseCommand.key_input('tab')

        # 输入数据第1个sql的数据库
        MysqlResult.input_content(self.first_monitor_db if self.first_monitor_db else MysqlResult.defaultMonitorDB)

        # 切换到数据第1个sql的数据库端口输入框
        MouseCommand.key_input('tab')

        # 输入数据第1个sql的数据库端口
        MysqlResult.input_content(self.first_monitor_port if self.first_monitor_port
                                  else MysqlResult.defaultMonitorPort)

        # 切换到数据第1个sql的数据库账号选择框
        MouseCommand.key_input('tab')

        # 选择第1个sql的数据库账号
        for i in range(int(self.first_monitor_user) if self.first_monitor_user else MysqlResult.defaultMonitorUser):
            MouseCommand.key_input('down_arrow')
        # 确认选择
        MouseCommand.key_input('enter')

        # 切换到数据第1个sql的sql输入框
        for j in range(3):
            MouseCommand.key_input('tab')

        # 输入第1个sql
        MysqlResult.input_content(self.first_monitor_sql if self.first_monitor_sql else MysqlResult.defaultMonitorSql)

        # 切换到数据第1个sql的名称输入框
        for j in range(3):
            MouseCommand.key_input('tab')

        # 输入第1个sql名称
        MysqlResult.input_content(self.first_monitor_name if self.first_monitor_name
                                  else MysqlResult.defaultMonitorName)

        # 切换到数据第2个sql的数据库地址输入框
        MouseCommand.key_input('tab')

        # 输入数据第2个sql的数据库地址
        MysqlResult.input_content(
            self.second_monitor_host if self.second_monitor_host else MysqlResult.defaultMonitorHost)

        # 切换到数据第2个sql的数据库输入框
        MouseCommand.key_input('tab')

        # 输入数据第2个sql的数据库
        MysqlResult.input_content(self.second_monitor_db if self.second_monitor_db else MysqlResult.defaultMonitorDB)

        # 切换到数据第2个sql的数据库端口输入框
        MouseCommand.key_input('tab')

        # 输入数据第2个sql的数据库端口
        MysqlResult.input_content(self.second_monitor_port if self.second_monitor_port
                                  else MysqlResult.defaultMonitorPort)

        # 切换到数据第2个sql的数据库账号选择框
        MouseCommand.key_input('tab')

        # 选择第2个sql的数据库账号
        for i in range(int(self.second_monitor_user) if self.second_monitor_user else self.defaultMonitorUser):
            MouseCommand.key_input('down_arrow')
        # 确认选择
        MouseCommand.key_input('enter')

        # 切换到数据第2个sql的sql输入框
        for j in range(3):
            MouseCommand.key_input('tab')

        # 输入第2个sql
        MysqlResult.input_content(self.second_monitor_sql if self.second_monitor_sql else MysqlResult.defaultMonitorSql)

        # 切换到数据第2个sql的名称输入框
        for j in range(3):
            MouseCommand.key_input('tab')

        # 输入第2个sql名称
        MysqlResult.input_content(self.second_monitor_name if self.second_monitor_name
                                  else MysqlResult.defaultMonitorName)

        # 切换到小数点精度选择
        MouseCommand.key_input('tab')

        # 选择小数精度
        monitor_decimal_precision = MysqlResult.defaultDecimalPrecision
        if self.decimal_precision and (4 >= self.decimal_precision > 0):
            monitor_decimal_precision = int(self.decimal_precision)
        for i in range(monitor_decimal_precision - 1):
            MouseCommand.key_input('right_arrow')
        # 选择保留有效小数
        MouseCommand.key_input('spacebar')

        # 切换到创建监控按钮
        MouseCommand.key_input('tab')

        # 创建监控
        MouseCommand.key_input('spacebar')

        # 关闭浏览器资源
        self.close_browser_resource()

        # 暂停5秒钟
        time.sleep(5)

    def update_monitor(self):
        """更新监控"""
        # 如果监控key为空，则直接返回
        if not MysqlResult.is_not_empty_str(self.monitor_key):
            return
        # 打开浏览器
        self.open_browser(MysqlResult.updateUrl + self.monitor_key)

        # 切换到监控名称的输入框
        for i in range(13):
            MouseCommand.key_input('tab')

        # 输入监控名称
        MysqlResult.input_if_not_empty(self.monitor_name)

        # 切换到时间粒度选择框
        MouseCommand.key_input('tab')

        # 选择时间粒度
        if MysqlResult.is_not_empty_str(self.time_space):
            for i in range(int(self.time_space) + 1):
                MouseCommand.key_input('right_arrow')

        # 切换到抽取时间输入框
        MouseCommand.key_input('tab')

        # 输入抽取时间
        MysqlResult.input_if_not_empty(self.query_time)

        # 切换到展示延时输入框
        MouseCommand.key_input('tab')

        # 输入展示延时
        MysqlResult.input_if_not_empty(self.show_delay_time)

        # 切换到展示单位输入框
        MouseCommand.key_input('tab')

        # 输入单位
        MysqlResult.input_if_not_empty(self.unit)

        # 切换到数据第1个sql的数据库地址输入框
        MouseCommand.key_input('tab')

        # 输入数据第1个sql的数据库地址
        MysqlResult.input_if_not_empty(self.first_monitor_host)

        # 切换到数据第1个sql的数据库输入框
        MouseCommand.key_input('tab')

        # 输入数据第1个sql的数据库
        MysqlResult.input_if_not_empty(self.first_monitor_db)

        # 切换到数据第1个sql的数据库端口输入框
        MouseCommand.key_input('tab')

        # 输入数据第1个sql的数据库端口
        MysqlResult.input_if_not_empty(self.first_monitor_port)

        # 切换到数据第1个sql的sql输入框
        MouseCommand.key_input('tab')

        # 输入第1个sql
        MysqlResult.input_if_not_empty(self.first_monitor_sql)

        # 切换到数据第1个sql的名称输入框
        for j in range(3):
            MouseCommand.key_input('tab')

        # 输入第1个sql名称
        MysqlResult.input_if_not_empty(self.first_monitor_name)

        # 切换到数据第2个sql的数据库地址输入框
        MouseCommand.key_input('tab')

        # 输入数据第2个sql的数据库地址
        MysqlResult.input_if_not_empty(self.second_monitor_host)

        # 切换到数据第2个sql的数据库输入框
        MouseCommand.key_input('tab')

        # 输入数据第2个sql的数据库
        MysqlResult.input_if_not_empty(self.second_monitor_db)

        # 切换到数据第2个sql的数据库端口输入框
        MouseCommand.key_input('tab')

        # 输入数据第2个sql的数据库端口
        MysqlResult.input_if_not_empty(self.second_monitor_port)

        # 切换到数据第2个sql的sql输入框
        MouseCommand.key_input('tab')

        # 输入第2个sql
        MysqlResult.input_if_not_empty(self.second_monitor_sql)

        # 切换到数据第2个sql的名称输入框
        for j in range(3):
            MouseCommand.key_input('tab')

        # 输入第2个sql名称
        MysqlResult.input_if_not_empty(self.second_monitor_name)

        # 切换到更新监控按钮
        MouseCommand.key_input('tab')

        # 更新监控
        MouseCommand.key_input('spacebar')

        # 关闭浏览器资源
        self.close_browser_resource()

        # 暂停5秒钟
        time.sleep(5)
