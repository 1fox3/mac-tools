#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import sys
import os
import time
import shutil
import pyperclip

from package.config.Env import get_env_config
from package.config.JD import get_jd_config
from package.tools.SystemInput.MouseCommand import MouseCommand
from package.tools.Help.Path import Path
from package.tools.Help.File import File


class Noah:
    """XShell操作"""
    ssh_type = 'Noah'

    @staticmethod
    def get_ssh_config(key=None):
        """获取ssh配置"""
        ssh_config_list = get_env_config('ssh_config', {})
        ssh_config = {}
        if Noah.ssh_type in ssh_config_list.keys():
            ssh_config = ssh_config_list[Noah.ssh_type]
        if key:
            key = str(key)
            if key in ssh_config.keys():
                return ssh_config[key]
            print(__file__ + str(sys._getframe().f_lineno) + ':no such config:' + key)
            return None
        else:
            return ssh_config

    @staticmethod
    def open_jd_jsp_conn():
        """连接京东跳板机"""
        erp_info = get_jd_config('erp_info')
        erp = erp_info.get('erp')
        erp_pwd = erp_info.get('password')
        noah_url = Noah.get_ssh_config('url')
        commands = {
            'ssh ' + erp + '@' + noah_url: 4,
            erp_pwd: 4,
        }
        Noah.handle_command(commands)
        commands = {
            # 选择堡垒机
            "1": 4,
        }
        Noah.handle_command(commands)
        commands = {
            # 选择账号
            "1": 4,
            # 多一次回车，清空界面
            "": 2
        }
        Noah.handle_command(commands)

    @staticmethod
    def handle_command(commands):
        """执行命令"""
        if isinstance(commands, list):
            for command in commands:
                Noah.input_command(command, 1)
        if isinstance(commands, dict):
            for command, sleep_time in commands.items():
                Noah.input_command(command, int(sleep_time))

    @staticmethod
    def sz_file(download_file, save_file):
        """通过sz命令从服务器上下载文件"""
        [download_path, download_name] = os.path.split(download_file)
        [save_path, save_name] = os.path.split(save_file)
        save_path = Path.path_suit_sys(save_path)
        save_file = Path.path_suit_sys(save_path, True) + save_name

        # 确保目录存在
        if not os.path.exists(save_path):
            os.system('mkdir ' + Path.path_suit_sys(save_path))
        # 删除当前的日志文件
        if os.path.exists(save_file):
            os.remove(save_file)
        # 命令顺序的数组
        commands = [
            'cd ' + download_path,
            'sz ' + download_name,
        ]
        Noah.handle_command(commands)

        path_point = (900, 625)  # 添写保存路径的位置
        MouseCommand.left_click(path_point)
        time.sleep(1)
        MouseCommand.multi_key_input(['ctrl', 'a'])
        MouseCommand.key_input('clear')
        save_commands = [
            save_file,
            ''
        ]
        Noah.handle_command(save_commands)

        # 监控文件是否已经下载完毕
        download_file_size = 0
        while True:
            current_download_file_size = os.path.getsize(save_file)
            if current_download_file_size != download_file_size:
                download_file_size = current_download_file_size
                time.sleep(2)
            else:
                break

    @staticmethod
    def input_command(command, sleep_time=1, end='\n'):
        pyperclip.copy(command)
        MouseCommand.multi_key_input(['command', 'v'])
        if end:
            MouseCommand.str_input(end)
        time.sleep(sleep_time)

    @staticmethod
    def get_log_file_full_path():
        log_file_path = Noah.get_ssh_config('log_path')
        log_file_path = Path.path_suit_sys(log_file_path, True)
        # 找到最新修改的日志文件
        lists = os.listdir(log_file_path)  # 列出目录的下所有文件和文件夹保存到lists
        lists.sort(key=lambda fn: os.path.getmtime(log_file_path + "\\" + fn))  # 按时间排序
        lists.reverse()
        log_file = time.strftime(Noah.get_ssh_config('log_format'), time.localtime())
        for log_file_name in lists:
            if log_file_name.find(log_file) >= 0:
                log_file = log_file_name
        log_file_full_path = log_file_path + log_file
        return log_file_full_path

    @staticmethod
    def is_need_verify_code():
        log_file_full_path = Noah.get_log_file_full_path()
        file_obj = File()
        log_file_obj = file_obj.open(log_file_full_path, 'r')
        log_file_size = os.path.getsize(log_file_full_path)
        log_file_obj.seek(log_file_size - 200)
        lines = log_file_obj.readlines()
        for line in lines:
            line = line.strip()
            if line.find('短信') >= 0 or line.find('短信') >= 0:
                return True
        return False

    @staticmethod
    def get_upload_url():
        MouseCommand.multi_key_input(['command', 'a'])
        time.sleep(0.2)
        MouseCommand.multi_key_input(['command', 'c'])
        lines = pyperclip.paste()
        lines = lines.split("\n")
        for line in lines:
            line = line.strip()
            if line.find('http') >= 0 and line.find('up.bastion.jd.com') >= 0:
                return line
        return ''

    @staticmethod
    def open_sftp():
        Noah.handle_command(
            [
                'cd /',
                'curl -s up.bastion.jd.com/file/up | bash'
            ]
        )
        time.sleep(4)

    @staticmethod
    def upload_files(upload_file_info_list):
        if len(upload_file_info_list) <= 0:
            return

        Noah.open_sftp()

        upload_url = Noah.get_upload_url()
        if not upload_url:
            return

        browser = get_env_config('browser', '')
        for up_load_file_info in upload_file_info_list:
            url = upload_url + up_load_file_info['dir'][1:] + '/'
            url = url.replace('//', '/')
            browser_resource = os.popen(browser + ' ' + url)
            time.sleep(1)
            MouseCommand.key_input('tab')
            time.sleep(1)
            MouseCommand.key_input('return')
            time.sleep(1)
            MouseCommand.multi_key_input(['command', 'shift', 'g'])
            time.sleep(1)
            Noah.input_command(up_load_file_info['local_file_path'], 1, '')
            # 按一下功能键，防止把return当文案处理
            MouseCommand.key_input('command')
            time.sleep(1)
            MouseCommand.key_input('return')
            time.sleep(1)
            MouseCommand.key_input('return')
            time.sleep(1)
            MouseCommand.key_input('tab')
            time.sleep(1)
            MouseCommand.key_input('return')
            time.sleep(1)
            MouseCommand.multi_key_input(['command', 'w'])
            time.sleep(1)
            browser_resource.close()

    @staticmethod
    def down_files(download_file_info_list):
        if len(download_file_info_list) <= 0:
            return

        Noah.open_sftp()

        upload_url = Noah.get_upload_url()
        if not upload_url:
            return

        browser = get_env_config('browser', '')
        for download_load_file_info in download_file_info_list:
            download_file = download_load_file_info['download_file']
            save_file = download_load_file_info['save_file']
            [download_path, download_name] = os.path.split(download_file)
            [save_path, save_name] = os.path.split(save_file)
            save_path = Path.path_suit_sys(save_path)
            save_file = Path.path_suit_sys(save_path, True) + save_name

            # 确保目录存在
            if not os.path.exists(save_path):
                print(save_path)
                os.system('mkdir -p ' + Path.path_suit_sys(save_path))
            # 删除当前的日志文件
            if os.path.exists(save_file):
                os.remove(save_file)

            # 获取文件临时下载路径
            download_path = Noah.get_ssh_config('download_path')
            temp_download_file = Path.path_suit_sys(download_path, True) + download_name
            url = upload_url + download_load_file_info['download_file']
            browser_resource = os.popen(browser + ' ' + url)
            # 监控文件是否已经下载完毕
            while True:
                if os.path.exists(temp_download_file):
                    break
                else:
                    time.sleep(2)
            shutil.move(temp_download_file, save_file)
            time.sleep(2)
            browser_resource.close()

    @staticmethod
    def close():
        MouseCommand.windows_system_command('window_close')
        time.sleep(2)
        MouseCommand.input_command('\n')
