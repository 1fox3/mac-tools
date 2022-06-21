#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import tkinter
from tkinter import ttk
from tkinter import messagebox

from package.config.GEServer import *
from package.config.GECode import GECode
from package.gui.workTools.BaseGui import BaseGui
from package.tools.Help.Path import Path
from package.tools.SSH.SSH import SSH
from package.config.Env import get_env_config


class VersionCopy(BaseGui):
    """代码文件同步"""
    # 默认目标版本
    default_des_version = 'lusongsong'
    # 服务器默认代码存放路径
    server_default_file_path = '/export/App/mba_jd_com'
    # 需要复制的文件路径
    version_paths = ['check_sign_', 'mba_']

    def __init__(self, root_tk):
        """首页初始化"""
        super().__init__(root_tk)
        # 业务类型
        self.service_combobox = ttk.Combobox(self.rootTk, width=30)
        # 服务器列表
        self.server_list_combobox = ttk.Combobox(self.rootTk, width=30, postcommand=self.get_server_list)
        # 默认复制版本
        self.default_ori_version = GECode['ge_ch_default_version'].replace('.', '')
        # 复制版本
        default_ori_version_str = tkinter.StringVar()
        default_ori_version_str.set(self.default_ori_version)
        self.ori_version_entry = tkinter.Entry(self.rootTk, width=20, textvariable=default_ori_version_str)
        # 目标版本
        default_des_version_str = tkinter.StringVar()
        default_des_version_str.set(VersionCopy.default_des_version)
        self.des_version_entry = tkinter.Entry(self.rootTk, width=20, textvariable=default_des_version_str)
        # 服务器列表选择框
        self.server_combobox = ttk.Combobox(self.rootTk, width=30)
        # 复制按钮
        self.copy_button = tkinter.Button(self.rootTk, command=self.copy, text='copy')
        # 清除按钮
        self.clear_button = tkinter.Button(self.rootTk, command=self.clear, text='clear')
        # 默认服务类型
        self.main_service = get_env_config('main_service', 'GE')

    def show_copy(self):
        """文件修改查询页面"""
        # 初始化界面
        service_label = tkinter.Label(self.rootTk, text='service:', padx=10)
        service_label.grid(row=0, column=0, sticky='n')
        self.service_combobox.grid(row=0, column=1, sticky='n')
        servers_label = tkinter.Label(self.rootTk, text='servers:', padx=10)
        servers_label.grid(row=0, column=2, sticky='n')
        self.server_list_combobox.grid(row=0, column=3, sticky='n')
        ori_version_label = tkinter.Label(self.rootTk, text='original:', padx=10)
        ori_version_label.grid(row=0, column=4, sticky='n')
        self.ori_version_entry.grid(row=0, column=5, sticky='n')
        des_version_label = tkinter.Label(self.rootTk, text='destination:', padx=10)
        des_version_label.grid(row=0, column=6, sticky='n')
        self.des_version_entry.grid(row=0, column=7, sticky='n')
        self.clear_button.grid(row=1, column=1, columnspan=3, sticky='s', ipadx=10)
        self.copy_button.grid(row=1, column=4, columnspan=3, sticky='s', ipadx=10)
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

    def get_server(self):
        """根据路径获取服务器"""
        service_list = ['GE']
        server_config_list = get_server_by_service(service_list)
        service_server_list = {}
        for service in server_config_list.keys():
            server_list = server_config_list[service]
            if server_list:
                for server in server_list:
                    server_config = server_list[server]
                    service_server_list[server] = server + ' ' + server_config['server_name']
        self.server_combobox['values'] = list(service_server_list.values())
        self.server_combobox.current(0)
        self.server_combobox.update()

    def copy(self):
        """复制"""
        self.ssh_server()
        # 命令顺序的数组
        commands = [
            'cd ' + self.server_default_file_path,  # 切换至代码路径
        ]
        ori_version_str = self.ori_version_entry.get()
        ori_version = ori_version_str if -1 == str.find(ori_version_str, '_') \
            else ori_version_str[0:str.find(ori_version_str, '_')]
        for file_path in VersionCopy.version_paths:
            des_path = file_path + 'dv' + ori_version + '_' + self.des_version_entry.get()
            # 删除目标版本
            commands.append('rm -r ' + des_path)
            # 复制版本
            commands.append('cp -rp ' + file_path + 'dv' + self.ori_version_entry.get() + ' '
                            + des_path)
        # 修改发送邮件目录需要的权限
        # commands.append('chmod 0777 -R ' + des_path + '/runtime/temp/core_email')
        SSH.handle_command(commands)
        self.online_debug()
        # SSH.close()
        messagebox.showinfo('版本复制', '已结束')

    def online_debug(self):
        """复制调试代码文件"""
        ori_version_str = self.ori_version_entry.get()
        ori_version = ori_version_str if -1 == str.find(ori_version_str, '_') \
            else ori_version_str[0:str.find(ori_version_str, '_')]
        version_path = VersionCopy.version_paths[-1] + 'dv' + ori_version + '_'\
                       + self.des_version_entry.get()
        online_debug_config = GECode['online_debug']
        file_path = online_debug_config['file_save_path']
        file_path = Path.path_suit_sys(file_path, True)
        files = online_debug_config['files']
        upload_file_info_list = []
        for file in files.keys():
            upload_file_info_list.append({
                'dir': files[file].replace('version_path', version_path),
                'local_file_path': file_path + file
            })
        SSH.upload_files(upload_file_info_list)

    def clear(self):
        """清除"""
        self.ssh_server()
        # 命令顺序的数组
        commands = [
            'cd ' + self.server_default_file_path,  # 切换至代码路径
        ]
        ori_version_str = self.ori_version_entry.get()
        ori_version = ori_version_str if -1 == str.find(ori_version_str, '_') \
            else ori_version_str[0:str.find(ori_version_str, '_')]
        for file_path in VersionCopy.version_paths:
            des_path = file_path + 'dv' + ori_version + '_' + self.des_version_entry.get()
            # 删除目标版本
            commands.append('rm -r ' + des_path)
        SSH.handle_command(commands)
        # SSH.close()
        messagebox.showinfo('版本清除', '已结束')

    def ssh_server(self):
        """连接服务器"""
        server_str = self.server_list_combobox['values'][self.server_list_combobox.current()]
        server_info = server_str.split(' ')
        ip = server_info[0]
        SSH.ssh_server(ip)

    def show(self):
        """显示代码文件同步初始界面"""
        self.show_copy()
