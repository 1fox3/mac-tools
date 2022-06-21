#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import sys
import time

import pyperclip

from package.config.Env import get_env_config
from package.config.GEServer import get_login_user
from package.tools.SSH.Noah import Noah
from package.tools.SystemInput.MouseCommand import MouseCommand


class SSH:
    """SSH操作"""

    @staticmethod
    def get_ssh_type():
        """获取ssh类型"""
        return get_env_config('ssh')

    @staticmethod
    def get_ssh_config(key=None):
        """获取ssh配置"""
        ssh_type = SSH.get_ssh_type()
        ssh_config_list = get_env_config('ssh_config', {})
        ssh_config = {}
        if ssh_type in ssh_config_list.keys():
            ssh_config = ssh_config_list[ssh_type]
        if key:
            key = str(key)
            if key in ssh_config.keys():
                return ssh_config[key]
            print(__file__ + str(sys._getframe().f_lineno) + ':no such config:' + key)
            return None
        else:
            return ssh_config

    @staticmethod
    def ssh_start():
        """启动ssh"""
        ssh_config = SSH.get_ssh_config()
        if ssh_config:
            ssh_config_keys = ssh_config.keys()
            if 'run_name' in ssh_config_keys:
                run_name = ssh_config['run_name']
                os.popen(run_name)
                time.sleep(3)
            else:
                print(__file__ + str(sys._getframe().f_lineno) + ':ssh config empty')
        else:
            print(__file__ + str(sys._getframe().f_lineno) + ':ssh not config')

    @staticmethod
    def ssh_jd_jsp():
        """连接京东跳板机"""
        SSH.ssh_start()
        ssh_class = SSH.ssh_class()
        if ssh_class:
            ssh_class.open_jd_jsp_conn()

    @staticmethod
    def ssh_class():
        ssh_type = str(SSH.get_ssh_type())
        if 'Noah' == ssh_type:
            return Noah
        else:
            print(__file__ + str(sys._getframe().f_lineno) + ':no class of' + ssh_type)
            return None

    @staticmethod
    def ssh_server(ip):
        """连接服务器"""
        login_info = get_login_user(ip)
        if login_info:
            login_user = login_info['user']
            login_password = login_info['password']
        SSH.ssh_jd_jsp()
        # 命令顺序的数组
        commands = {
            'ssh ' + login_user + '@' + ip: 3,  # 连接服务器
            login_password: 3,  # 服务器密码
        }
        SSH.handle_command(commands)

    @staticmethod
    def handle_command(commands):
        """执行命令"""
        if isinstance(commands, list):
            for command in commands:
                SSH.input_command(command, 1)
        if isinstance(commands, dict):
            for command, sleep_time in commands.items():
                SSH.input_command(command, int(sleep_time))

    @staticmethod
    def input_command(command, sleep_time=1, end='\n'):
        pyperclip.copy(command + end)
        MouseCommand.multi_key_input(['command', 'v'])
        time.sleep(sleep_time)

    @staticmethod
    def sz_file(file_path, save_path):
        SSH.down_files([
            {
                'download_file': file_path,
                'save_file': save_path,
            }
        ])

    @staticmethod
    def upload_files(upload_file_info_list):
        """上传文件"""
        ssh_class = SSH.ssh_class()
        if ssh_class:
            ssh_class.upload_files(upload_file_info_list)

    @staticmethod
    def down_files(download_file_info_list):
        """上传文件"""
        ssh_class = SSH.ssh_class()
        if ssh_class:
            ssh_class.down_files(download_file_info_list)
