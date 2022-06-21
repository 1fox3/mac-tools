#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import tkinter
from tkinter import ttk

from package.config.GEDb import *
from package.gui.workTools.BaseGui import BaseGui
from package.tools.SSH.SSH import SSH


class GEDbLogin(BaseGui):
    """登录黄金眼mysql服务器"""
    # 数据库平台类型
    platformTypeConfig = {
        '主站': 'main',
        '泰国': 'th',
        '印尼': 'id',
        'CK': 'ck',
    }
    # 数据库类型
    dbTypeConfig = {
        '主': 0,
        '从': 1,
    }

    # 数据库环境类型
    envTypeConfig = {
        '线上': 0,
        '预发': 1,
    }

    # 登录服务器ip
    loginServerIp = '11.55.115.115'
    # ck登录服务器ip
    ckLoginServerIp = '10.181.48.19'

    def __init__(self, root_tk):
        """首页初始化"""
        super().__init__(root_tk)
        # 数据库平台类型
        self.platform_type_combobox = ttk.Combobox(self.rootTk, width=10)
        # 数据库主从类型
        self.db_type_combobox = ttk.Combobox(self.rootTk, width=10)
        # 数据库环境类型
        self.env_type_combobox = ttk.Combobox(self.rootTk, width=10)
        # 数据库列表
        self.db_list_combobox = ttk.Combobox(self.rootTk, width=30, postcommand=self.get_db_list)
        self.login_button = tkinter.Button(self.rootTk, command=self.login, text='login')

    def show_login(self):
        """服务器登录页面"""
        # 初始化界面
        platform_type_label = tkinter.Label(self.rootTk, text='platform type:', padx=10)
        platform_type_label.grid(row=0, column=0, sticky='n')
        self.platform_type_combobox.grid(row=0, column=1, sticky='n')
        db_type_label = tkinter.Label(self.rootTk, text='db type:', padx=10)
        db_type_label.grid(row=0, column=2, sticky='n')
        self.db_type_combobox.grid(row=0, column=3, sticky='n')
        env_type_label = tkinter.Label(self.rootTk, text='env type:', padx=10)
        env_type_label.grid(row=0, column=4, sticky='n')
        self.env_type_combobox.grid(row=0, column=5, sticky='n')
        db_list_label = tkinter.Label(self.rootTk, text='db:', padx=10)
        db_list_label.grid(row=0, column=6, sticky='n')
        self.db_list_combobox.grid(row=0, column=7, sticky='n')
        self.login_button.grid(row=1, column=0, sticky='s', ipadx=10)
        # 加载数据库平台类型列表
        self.platform_type_combobox['values'] = list(GEDbLogin.platformTypeConfig.keys())
        self.platform_type_combobox.current(0)
        self.platform_type_combobox.update()
        # 加载数据库类型列表
        self.db_type_combobox['values'] = list(GEDbLogin.dbTypeConfig.keys())
        self.db_type_combobox.current(0)
        self.db_type_combobox.update()
        # 加载数据库类型列表
        self.env_type_combobox['values'] = list(GEDbLogin.envTypeConfig.keys())
        self.env_type_combobox.current(0)
        self.env_type_combobox.update()
        # 加载数据库列表
        self.get_db_list()
        self.rootTk.pack()

    def get_db_list(self):
        """数据库列表"""
        platform_type = self.get_platform_type()
        db_type = self.get_db_type()
        env_type = self.get_env_type()
        db_config_list = get_db_list(
            {
                'platform_type': platform_type,
                'db_type': db_type,
                'env_type': env_type
            }
        )
        db_list = []
        for db_config in db_config_list:
            db_list.append(db_config["db_name"])
        self.db_list_combobox['values'] = db_list
        self.db_list_combobox.current(0)
        self.db_list_combobox.update()

    def get_platform_type(self):
        """获取数据平台类型"""
        platform_type_str = self.platform_type_combobox['values'][self.platform_type_combobox.current()]
        return GEDbLogin.platformTypeConfig[platform_type_str]

    def get_db_type(self):
        """获取数据类型"""
        db_type_str = self.db_type_combobox['values'][self.db_type_combobox.current()]
        return GEDbLogin.dbTypeConfig[db_type_str]

    def get_env_type(self):
        """获取数据类型"""
        env_type_str = self.env_type_combobox['values'][self.env_type_combobox.current()]
        return GEDbLogin.envTypeConfig[env_type_str]

    def get_db_name(self):
        """获取数据库名"""
        return self.db_list_combobox['values'][self.db_list_combobox.current()]

    def login_db_config(self):
        """获取需要登录的数据库配置"""
        platform_type = self.get_platform_type()
        db_type = self.get_db_type()
        env_type = self.get_env_type()
        db_name_str = self.get_db_name()
        db_config_list = get_db_list(
            {
                'platform_type': platform_type,
                'db_type': db_type,
                'env_type': env_type,
                'db_name': db_name_str
            }
        )
        return db_config_list[0]

    def login(self):
        """登录服务器"""
        db_config = self.login_db_config()
        ip = GEDbLogin.loginServerIp
        if 'ck' == db_config.get('platform_type'):
            ip = GEDbLogin.ckLoginServerIp
        SSH.ssh_server(ip)
        login_command = get_login_command(db_config)
        commands = {
            login_command: 3,
            "use " + db_config["db"] + ";": 1,
            "set charset utf8;": 1,
        }
        SSH.handle_command(commands)

    def show(self):
        """显示日志下载界面"""
        self.show_login()
