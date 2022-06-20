#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import tkinter

from package.gui.workTools.rsyncCodeFile.RsyncCodeFile import RsyncCodeFile
# from package.gui.workTools.version.VersionCopy import VersionCopy
# from package.gui.workTools.logs.LogsDownload import LogsDownload
from package.gui.workTools.servers.ServersLogin import ServersLogin
# from package.gui.workTools.systemInput.SystemInputLog import SystemInputLog
# from package.gui.workTools.systemInput.SystemInputRepeat import SystemInputRepeat
# from package.gui.workTools.gEDb.GEDbLogin import GEDbLogin
# from package.gui.workTools.gEDb.GEDbTableRsync import GEDbTableRsync
# from package.gui.workTools.gEDb.GEDbTableDataDownload import GEDbTableDataDownload
# from package.gui.workTools.version.VersionLocalDebug import VersionLocalDebug
from package.gui.workTools.string.StringHandle import StringHandle
# from package.gui.workTools.dinner.DinnerAdd import DinnerAdd
# from package.gui.workTools.dinner.DinnerChoose import DinnerChoose
# from package.gui.workTools.javaDaoTool.JavaDaoTool import JavaDaoTool
# from package.gui.workTools.version.VersionLocalIgnore import VersionLocalIgnore


class HomePage:
    """办公工具的首页"""
    title = '京东办公工具'  # 标题
    windowSize = '1600x700'  # 窗口初始化大小
    initPos = '+200+200'  # 窗口初始化位置
    current_gui_obj = None  # 当前组件类

    def __init__(self):
        """首页初始化"""
        self.rootTk = None
        self.create_root()

    def create_root(self):
        """创建主控件"""
        self.rootTk = tkinter.Tk(screenName='京东办公工具')
        self.rootTk.title(self.title)
        self.rootTk.geometry(self.windowSize + self.initPos)
        self.add_menu()

    def home_clear(self):
        """清空页面"""
        if None is not self.current_gui_obj:
            self.current_gui_obj.hide()

    def refresh_page(self, gui_class):
        """刷新界面"""
        self.home_clear()
        self.current_gui_obj = gui_class(self.rootTk)
        self.current_gui_obj.show()

    def add_menu(self):
        """添加菜单栏"""
        tk_menu = tkinter.Menu(self.rootTk, tearoff=False)
        menu_config = {
            'RsyncCodeFile': {
                'label': 'RsyncCodeFile',
                'command': self.rsync_code_file
            },
            # 'Version': {
            #     'label': 'Version',
            #     'sub_menu': [
            #         {
            #             'label': 'Copy',
            #             'command': self.version_copy
            #         },
            #         {
            #             'label': 'Local Debug',
            #             'command': self.version_local_debug
            #         },
            #         {
            #             'label': 'Local Ignore',
            #             'command': self.version_local_ignore
            #         },
            #     ],
            # },
            # 'Logs': {
            #     'label': 'Logs',
            #     'sub_menu': [
            #         {
            #             'label': 'download',
            #             'command': self.logs_download
            #         },
            #     ],
            # },
            'Servers': {
                'label': 'Servers',
                'sub_menu': [
                    {
                        'label': 'login',
                        'command': self.servers_login
                    },
                ],
            },
            # 'DB': {
            #     'label': 'DB',
            #     'sub_menu': [
            #         {
            #             'label': 'login',
            #             'command': self.ge_db_login
            #         },
            #         {
            #             'label': 'table rsync',
            #             'command': self.ge_db_table_rsync
            #         },
            #         {
            #             'label': 'data download',
            #             'command': self.ge_db_data_download
            #         },
            #     ],
            # },
            # 'SystemInput': {
            #     'label': 'SystemInput',
            #     'sub_menu': [
            #         {
            #             'label': 'log',
            #             'command': self.system_input_log
            #         },
            #         {
            #             'label': 'repeat',
            #             'command': self.system_input_repeat
            #         },
            #     ],
            # },
            'String': {
                'label': 'String',
                'sub_menu': [
                    {
                        'label': 'handle',
                        'command': self.string_handle
                    },
                ],
            },
            # 'Dinner': {
            #     'label': 'Dinner',
            #     'sub_menu': [
            #         {
            #             'label': 'add',
            #             'command': self.dinner_add
            #         },
            #         {
            #             'label': 'choose',
            #             'command': self.dinner_choose
            #         },
            #     ],
            # },
            # 'JavaDaoTool': {
            #     'label': 'JavaDaoTool',
            #     'command': self.java_dao_tool
            # },
        }
        self.rootTk.config(menu=tk_menu)
        for menu_key in menu_config.keys():
            menu_option = menu_config[menu_key]
            if ('sub_menu' not in menu_option.keys()) or (not menu_option['sub_menu']):
                tk_menu.add_command(menu_option)
            else:
                sub_menu = menu_option['sub_menu']
                sub_menu_tk = tkinter.Menu(self.rootTk, tearoff=False)
                for sub_menu_option in sub_menu:
                    sub_menu_tk.add_command(sub_menu_option)
                menu_option['menu'] = sub_menu_tk
                menu_option.pop('sub_menu')
                tk_menu.add_cascade(menu_option)

    def show(self):
        """显示初始界面"""
        self.rsync_code_file()
        self.rootTk.mainloop()

    def rsync_code_file(self):
        """启动同步代码文件页面"""
        self.refresh_page(RsyncCodeFile)
    #
    # def version_copy(self):
    #     """启动版本复制页面"""
    #     self.refresh_page(VersionCopy)
    #
    # def logs_download(self):
    #     """启动版本复制页面"""
    #     self.refresh_page(LogsDownload)

    def servers_login(self):
        """登录服务器"""
        self.refresh_page(ServersLogin)

    # def system_input_log(self):
    #     """记录系统输入操作"""
    #     self.refresh_page(SystemInputLog)
    #
    # def system_input_repeat(self):
    #     """重放系统输入操作"""
    #     self.refresh_page(SystemInputRepeat)
    #
    # def ge_db_login(self):
    #     """登录数据库"""
    #     self.refresh_page(GEDbLogin)

    # def ge_db_table_rsync(self):
    #     """数据表同步"""
    #     self.refresh_page(GEDbTableRsync)
    #
    # def ge_db_data_download(self):
    #     """数据表数据下载"""
    #     self.refresh_page(GEDbTableDataDownload)
    #
    # def version_local_debug(self):
    #     """启动版本本地调试页面"""
    #     self.refresh_page(VersionLocalDebug)

    def string_handle(self):
        """启动字符串处理页面"""
        self.refresh_page(StringHandle)

    # def dinner_add(self):
    #     """午饭添加"""
    #     self.refresh_page(DinnerAdd)
    #
    # def dinner_choose(self):
    #     """午饭选择"""
    #     self.refresh_page(DinnerChoose)
    #
    # def java_dao_tool(self):
    #     """java数据表工具选择"""
    #     self.refresh_page(JavaDaoTool)
    #
    # def version_local_ignore(self):
    #     """启动版本本地调试页面"""
    #     self.refresh_page(VersionLocalIgnore)
