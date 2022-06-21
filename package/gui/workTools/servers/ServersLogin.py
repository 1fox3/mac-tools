#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import tkinter
from tkinter import ttk
from tkinter import messagebox

from package.config.GEServer import *
from package.config.Env import get_env_config
from package.gui.workTools.BaseGui import BaseGui
from package.tools.Help.Path import Path
from package.tools.Help.File import File
from package.tools.SSH.SSH import SSH
from package.config.JD import get_jd_config


class ServersLogin(BaseGui):
    """登录服务器"""
    # 默认代码搜索路径
    default_login_path = '/export/App'
    default_moba_xterm_session_file_path = '/Users/lusongsong/Logs/MobaXterm/'

    def __init__(self, root_tk):
        """首页初始化"""
        super().__init__(root_tk)
        # 业务类型
        self.service_combobox = ttk.Combobox(self.rootTk, width=30)
        # 服务器列表
        self.server_list_combobox = ttk.Combobox(self.rootTk, width=30, postcommand=self.get_server_list)
        # 代码文件路径
        default_login_path_str = tkinter.StringVar()
        default_login_path_str.set(ServersLogin.default_login_path)
        # 本地搜索路径
        self.login_path_entry = tkinter.Entry(self.rootTk, width=75, textvariable=default_login_path_str)
        # 登录按钮
        self.login_button = tkinter.Button(self.rootTk, command=self.login, text='login')
        self.create_moba_xterm_session_button = tkinter.Button(self.rootTk, command=self.create_moba_xterm_session,
                                                               text='create MobaXterm session')
        # 默认服务类型
        self.main_service = get_env_config('main_service', 'GE')

    def show_login(self):
        """服务器登录页面"""
        # 初始化界面
        service_label = tkinter.Label(self.rootTk, text='service:', padx=10)
        service_label.grid(row=0, column=0, sticky='n')
        self.service_combobox.grid(row=0, column=1, sticky='n')
        servers_label = tkinter.Label(self.rootTk, text='servers:', padx=10)
        servers_label.grid(row=0, column=2, sticky='n')
        self.server_list_combobox.grid(row=0, column=3, sticky='n')
        login_path_label = tkinter.Label(self.rootTk, text='login path:', padx=10)
        login_path_label.grid(row=1, column=0, sticky='n')
        self.login_path_entry.grid(row=1, column=1, columnspan=3, sticky='n')
        self.login_button.grid(row=2, columnspan=2, sticky='s', ipadx=10)
        self.create_moba_xterm_session_button.grid(row=2, columnspan=4, sticky='s', ipadx=10)
        # 加载服务列表
        self.get_server_service()
        # 加载服务器列表
        self.get_server_list()
        self.rootTk.pack()

    def get_server_service(self):
        """根据服务器服务类型列表"""
        server_config_list = get_server()
        service_list = []
        main_index = 0
        for server_config in server_config_list.values():
            service = server_config['service'] if 'service' in server_config.keys() else ''
            if service and service not in service_list:
                service_list.append(service)
                if service == self.main_service:
                    main_index = len(service_list) - 1
        self.service_combobox['values'] = service_list
        self.service_combobox.current(main_index)
        self.service_combobox.update()

    def get_server_list(self):
        """根据服务器类型列表"""
        service_str = self.service_combobox['values'][self.service_combobox.current()]
        server_config_list = get_server_by_service(service_str)
        service_server_list = {}
        for service in server_config_list.keys():
            server_list = server_config_list[service]
            if server_list:
                for server in server_list:
                    server_config = server_list[server]
                    service_server_list[server] = server + ' ' + server_config['server_name']
        self.server_list_combobox['values'] = list(service_server_list.values())
        self.server_list_combobox.current(0)
        self.server_list_combobox.update()

    def login(self):
        """登录服务器"""
        server_str = self.server_list_combobox['values'][self.server_list_combobox.current()]
        server_info = server_str.split(' ')
        ip = server_info[0]
        SSH.ssh_server(ip)
        self.change_path()

    def change_path(self):
        """切换目录"""
        path = self.login_path_entry.get()
        path = path.replace('\\', '/')
        # 切换目录
        commands = [
            'cd ' + path,
        ]
        SSH.handle_command(commands)

    def create_moba_xterm_session(self):
        """登录服务器"""
        service_str = self.service_combobox['values'][self.service_combobox.current()]
        server_config_list = get_server_by_service(service_str)
        session_str = "[Bookmarks]\n"
        session_str += 'SubRep=' + service_str
        session_str += "\nImgNum=41\n"
        erp_info = get_jd_config('erp_info')
        erp = erp_info.get('erp')
        noah_url = get_env_config(['ssh_config', 'Noah', 'url'])
        for service in server_config_list.keys():
            server_list = server_config_list[service]
            if server_list:
                for server in server_list:
                    server_config = server_list[server]
                    ip = server_config['ip']
                    login_user = server_config['login_user']
                    session_str += server_config['server_type'] + "_" + ip + " (" + login_user\
                                   + ")= #109#0%" + ip + "%22%" + login_user\
                                   + "%%-1%-1%%"\
                                   + noah_url\
                                   + "%22%"\
                                   + erp\
                                   + "%0%0%0%%%-1%0%0%0%%1080%%0%0%1#MobaFont%10%0%0%0%15%236,236,236%0,0,0%180,180" \
                                     ",192%0%-1%0%%xterm%-1%0%0,0,0%54,54,54%255,96,96%255,128,128%96,255,96%128,255" \
                                     ",128%255,255,54%255,255,128%96,96,255%128,128,255%255,54,255%255,128,255%54" \
                                     ",255,255%128,255,255%236,236,236%255,255,255%80%24%0%1%-1%<none>%%0#0#\n"
        # 确保目录存在
        if not os.path.exists(ServersLogin.default_moba_xterm_session_file_path):
            os.system('mkdir ' + Path.path_suit_sys(ServersLogin.default_moba_xterm_session_file_path))
        file_path = ServersLogin.default_moba_xterm_session_file_path + service_str + '.mxtsessions'
        print(file_path)
        file_obj = File().open(file_path, 'w+')
        file_obj.write(session_str)
        messagebox.showinfo('创建成功', file_path)

    def show(self):
        """显示日志下载界面"""
        self.show_login()
