#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import tkinter
from tkinter import ttk
from tkinter import messagebox

from package.config.GECode import GECode
from package.config.GEServer import *
from package.tools.Git.Git import Git
from package.tools.SSH.SSH import SSH
from package.tools.Help.Path import Path


class RsyncCodeFile:
    """代码文件同步"""
    # 默认代码搜索路径
    default_file_path = '/Users/lusongsong/Code/php/mobile_mba'
    # 服务器默认代码存放路径
    server_default_file_path = '/export/App'
    # 代码文件tree配置
    code_file_column = {
        'mode': {
            'text': '类型',
            'width': 100,
        },
        'file_path': {
            'text': '路径',
            'width': 800,
        },
        'tag': {
            'text': '选择',
            'width': 100
        },
        'file_m_time': {
            'text': '修改时间',
            'width': 200,
        }
    }
    # 路径和服务器类型
    path_server_config = {
        'mobile_mba': 'GE',
        'mobile_mba_monitor': 'PHP_MONITOR',
        'th_ge_server': 'GE_TH',
        'id_ge_server': 'GE_ID',
        'th_ge_monitor': 'TH_GE_MONITOR',
        'id_ge_monitor': 'ID_GE_MONITOR',
        'ge_jdme_server': 'GE_JD_ME',
    }
    # 目录下修改的文件列表
    git_files = {}
    # 文件选中的tag
    selected_tag = 'selected'

    def __init__(self, root_tk):
        """首页初始化"""
        self.rootTk = root_tk
        # 代码文件路径
        default_path_str = tkinter.StringVar()
        default_path_str.set(RsyncCodeFile.default_file_path)
        # 本地搜索路径
        self.path_entry = tkinter.Entry(self.rootTk, width=100, textvariable=default_path_str)
        # 服务器列表选择框
        self.server_combobox = ttk.Combobox(self.rootTk, width=30)
        # 搜索按钮
        self.search_button = tkinter.Button(self.rootTk, command=self.search_file, text='search')
        # 文件列表
        self.code_file_tree = ttk.Treeview(self.rootTk, selectmode="extended")
        # 服务器代码原始路径
        replace_ori_path_str = tkinter.StringVar()
        replace_ori_path_str.set('/export/App/mba_jd_com/mba_dv' + GECode['ge_ch_default_version'].replace('.', ''))
        self.replace_ori_path_entry = tkinter.Entry(self.rootTk, width=50, textvariable=replace_ori_path_str)
        # 服务器代码替换路径
        replace_des_path_str = tkinter.StringVar()
        replace_des_path_str.set('/export/App/mba_jd_com/mba_dv' + GECode['ge_ch_default_version'].replace('.', '') + '_lusongsong')
        self.replace_des_path_entry = tkinter.Entry(self.rootTk, width=50, textvariable=replace_des_path_str)

    def show_search(self):
        """文件修改查询页面"""
        path_label = tkinter.Label(self.rootTk, text='path:', padx=10)
        path_label.grid(row=0, column=0, sticky='n')
        self.path_entry.grid(row=0, column=1, sticky='n')
        server_label = tkinter.Label(self.rootTk, text='server:', padx=10)
        server_label.grid(row=0, column=2, sticky='n')
        self.server_combobox.grid(row=0, column=3, sticky='n')
        self.get_server()
        self.search_button.grid(row=1, columnspan=4, sticky='s', ipadx=10)
        self.rootTk.update()

    def get_server(self):
        """根据路径获取服务器"""
        path = self.get_local_path(self.path_entry)
        service_list = []
        path = path if isinstance(path, str) else ''
        path_arr = path.split('\\')
        for sub_path in RsyncCodeFile.path_server_config.keys():
            if sub_path in path_arr:
                service_list.append(RsyncCodeFile.path_server_config[sub_path])
        if not service_list:
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

    def search_file(self):
        """查询文件修改"""
        path = self.get_local_path(self.path_entry)
        self.get_server()
        self.git_files = {}
        git_files = Git.get_change_file_info(path)
        for file_info in git_files:
            file_info['tag'] = ''
            self.git_files[file_info['file_path']] = file_info
        self.show_code_file_tree()
        replace_ori_path_label = tkinter.Label(self.rootTk, text='original path:', padx=10)
        replace_ori_path_label.grid(row=3, column=0, sticky='n')
        self.replace_ori_path_entry.grid(row=3, column=1, sticky='n')
        replace_des_path_label = tkinter.Label(self.rootTk, text='des path:', padx=10)
        replace_des_path_label.grid(row=3, column=2, sticky='n')
        self.replace_des_path_entry.grid(row=3, column=3, sticky='n')
        rsync_button = tkinter.Button(self.rootTk, command=self.rsync_file, text='rsync')
        rsync_button.grid(row=4, columnspan=4, sticky='s', ipadx=10)
        self.rootTk.update()

    @staticmethod
    def get_local_path(obj, end=''):
        """获取文件路径"""
        return Path.path_suit_sys(obj.get(), True)

    @staticmethod
    def get_server_path(obj, end=''):
        """获取文件路径"""
        path = obj.get()
        return path.replace('\\', '/') + end

    def show_code_file_tree(self):
        """显示文件修改列表"""
        self.clear_code_file_tree()
        self.code_file_tree.grid_remove()
        git_files = list(self.git_files.values())
        if git_files:
            code_file_column_keys = list(RsyncCodeFile.code_file_column.keys())
            code_file_tree_columns = code_file_column_keys
            self.code_file_tree['columns'] = code_file_tree_columns
            for code_file_column_key in code_file_tree_columns:
                code_file_column_config = RsyncCodeFile.code_file_column[code_file_column_key]
                code_file_column_config_keys = code_file_column_config.keys()
                if 'width' in code_file_column_config_keys:
                    self.code_file_tree.column(code_file_column_key, width=code_file_column_config['width'])
                if 'text' in code_file_column_config_keys:
                    self.code_file_tree.heading(code_file_column_key, text=code_file_column_config['text'])
            for i in range(0, len(git_files)):
                git_file = git_files[i]
                values = [git_file[code_file_column_key] for code_file_column_key in code_file_tree_columns]
                self.code_file_tree.insert('', i, text=str(i + 1), values=values, tag=git_file['tag'])
            self.code_file_tree.tag_configure(self.selected_tag, background='#7B68EE')
            self.code_file_tree.grid(row=2, columnspan=6, sticky='s', ipadx=10)
            self.code_file_tree.bind('<ButtonRelease-1>', self.choose_file)

    def clear_code_file_tree(self):
        """清空文件列表"""
        items = self.code_file_tree.get_children()
        for item in items:
            self.code_file_tree.delete(item)

    def choose_file(self, event):
        """处理用户点击文件列表事件"""
        for item in self.code_file_tree.selection():
            item_info = dict(self.code_file_tree.item(item).items())
            item_values = item_info['values']
            file_path = item_values[1]
            if self.selected_tag != self.git_files[file_path]['tag']:
                self.git_files[file_path]['tag'] = self.selected_tag
            else:
                self.git_files[file_path]['tag'] = ''
        self.show_code_file_tree()
        self.rootTk.update()

    def rsync_file(self):
        """同步文件"""
        rsync_files = self.get_rsync_file()
        if rsync_files:
            local_path = self.get_local_path(self.path_entry, '/')
            server_path = self.server_default_file_path
            replace_ori_path = self.get_server_path(self.replace_ori_path_entry, '/')
            replace_des_path = self.get_server_path(self.replace_des_path_entry, '/')
            # 需要上传的文件
            upload_file_info_list = []
            # 需要删除的文件
            delete_file_list = []
            # 需要添加的文件目录
            add_dir_list = []
            for path in rsync_files.keys():
                server_dir = server_path + '/' + path
                # 路径替换
                if replace_des_path and server_dir.startswith(replace_ori_path):
                    server_dir = server_dir.replace(replace_ori_path, replace_des_path)
                files = rsync_files[path]
                for file in files:
                    if 'deleted' == file['mode']:
                        delete_file_list.append(server_dir + '/' + file['file_name'])
                        continue
                    if 'added' == file['mode'] or 'new file' == file['mode']:
                        add_dir_list.append(server_dir)
                    upload_file_info_list.append({
                        'dir': server_dir,
                        'local_file_path': Path.path_suit_sys(local_path + path + '/' + file['file_name']),
                    })
            self.upload_file(delete_file_list, add_dir_list, upload_file_info_list)
            messagebox.showinfo('文件上传', '已结束')

    def upload_file(self, delete_file_list, add_dir_list, upload_file_info_list):
        """上传文件"""
        # 登录服务器
        self.ssh_server()
        # 切到根目录
        SSH.input_command('cd /')
        # 删除文件
        if len(delete_file_list) > 0:
            for delete_file in delete_file_list:
                SSH.input_command('rm ' + delete_file)
        # 添加文件
        if len(add_dir_list) > 0:
            for add_dir in set(add_dir_list):
                SSH.input_command('mkdir -p ' + add_dir)
        # 上传文件
        SSH.upload_files(upload_file_info_list)

    def get_rsync_file(self):
        """获取需要同步的文件"""
        git_files = list(self.git_files.values())
        rsync_files = {}
        if git_files:
            for git_file in git_files:
                tag = git_file['tag']
                if self.selected_tag == tag:
                    file_path = git_file['file_path'].strip()
                    [path, file_name] = os.path.split(file_path)
                    if path not in rsync_files.keys():
                        rsync_files[path] = []
                    rsync_files[path].append(
                        {
                            'file_name': file_name,
                            'mode': git_file['mode'],
                        }
                    )
        return rsync_files

    def ssh_server(self):
        """连接服务器"""
        server_str = self.server_combobox['values'][self.server_combobox.current()]
        server_info = server_str.split(' ')
        ip = server_info[0]
        SSH.ssh_server(ip)

    def show(self):
        """显示代码文件同步初始界面"""
        self.show_search()
