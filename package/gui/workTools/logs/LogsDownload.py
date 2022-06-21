#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import tkinter
from tkinter import ttk
import os
import time
import datetime

from package.config.GEServer import *
from package.gui.workTools.BaseGui import BaseGui
from package.tools.SSH.SSH import SSH
from package.config.Env import get_env_config


class LogsDownload(BaseGui):
    """日志下载"""
    logFilterKey = 'id'
    logFileDownloadPath = '/Users/lusongsong/Downloads/'
    localPHPCodePath = '/Users/lusongsong/Code/php/1fox3/www/app/cron/mba/log/'
    logTypeConfig = {
        'request': {
            'log_file_name': 'http_api_reqest_and_response.log',
            'log_table': 't_request_log',
            'save_to_db_script': localPHPCodePath + 'LogFileToDb.php',
            'log_to_postman_script': localPHPCodePath + 'LogToPostMan.php'
        },
        'local': {
            'log_file_name': 'local_http_api.log',
            'log_table': 't_local_request_log',
            'save_to_db_script': localPHPCodePath + 'LocalLogFileToDb.php',
            'log_to_postman_script': localPHPCodePath + 'LocalLogToPostMan.php'
        },
        'javaMonitorRequest': {
            'log_file_name': 'java_monitor_http_request_log',
            'log_table': 't_java_monitor_request_log',
            'save_to_db_script': localPHPCodePath + 'JavaMonitorRequestLogFileToDb.php',
            'log_to_postman_script': localPHPCodePath + 'JavaMonitorRequestLogToPostMan.php'
        },
        'prestoRequest': {
            'log_file_name': 'query.log',
            'log_table': 't_presto_request_log',
            'save_to_db_script': localPHPCodePath + 'PrestoRequestLogFileToDb.php',
            'log_to_postman_script': localPHPCodePath + 'PrestoRequestLogToPostMan.php'
        },
        'phpMonitorRequest': {
            'log_file_name': 'php_monitor_http_request.log',
            'log_table': 't_php_monitor_request_log',
            'save_to_db_script': localPHPCodePath + 'PHPMonitorRequestLogFileToDb.php',
            'log_to_postman_script': localPHPCodePath + 'PHPMonitorRequestLogToPostMan.php'
        },
    }

    def __init__(self, root_tk):
        """首页初始化"""
        super().__init__(root_tk)
        # 业务类型
        self.service_combobox = ttk.Combobox(self.rootTk, width=30)
        # 服务器列表
        self.server_list_combobox = ttk.Combobox(self.rootTk, width=30, postcommand=self.get_server_list)
        # 日志类型列表
        self.log_type_combobox = ttk.Combobox(self.rootTk, width=30)
        # 复制按钮
        self.download_button = tkinter.Button(self.rootTk, command=self.logs_download, text='download')
        # 将日志导入到数据库中
        # self.logs_to_db_button = tkinter.Button(self.rootTk, command=self.logs_to_db, text='logs to db')
        # 当前下载的日志文件路径
        self.current_download_log_file_path = ''
        # 日志日期筛选条件
        self.log_date_entry = tkinter.Entry(self.rootTk, width=30)
        # 日志筛选条件
        self.log_filter_entry = tkinter.Entry(self.rootTk, width=32)
        # 将日志导入到postman
        self.logs_to_postman_button = tkinter.Button(self.rootTk, command=self.logs_to_postman, text='logs to postman')
        # 服务器类型
        self.server_dev_value = tkinter.IntVar()
        self.server_test_value = tkinter.IntVar()
        self.server_online_value = tkinter.IntVar()
        self.server_dev_check = tkinter.Checkbutton(self.rootTk, text='ALL DEV SERVERS', variable=self.server_dev_value)
        self.server_test_check = tkinter.Checkbutton(self.rootTk, text='ALL TEST SERVERS',
                                                     variable=self.server_test_value)
        self.server_online_check = tkinter.Checkbutton(self.rootTk, text='ALL ONLINE SERVERS',
                                                       variable=self.server_online_value)
        # 默认服务类型
        self.main_service = get_env_config('main_service', 'GE')

    def show_download(self):
        """日志下载界面"""
        service_label = tkinter.Label(self.rootTk, text='service:')
        service_label.grid(row=0, column=0, sticky='n')
        self.service_combobox.grid(row=0, column=1, sticky='n')
        servers_label = tkinter.Label(self.rootTk, text='servers:')
        servers_label.grid(row=0, column=2, sticky='n')
        self.server_list_combobox.grid(row=0, column=3, sticky='n')
        self.server_online_check.grid(row=0, column=4, sticky='n')
        self.server_test_check.grid(row=0, column=5, sticky='n')
        self.server_dev_check.grid(row=0, column=6, sticky='n')
        log_type_label = tkinter.Label(self.rootTk, text='log type:')
        log_type_label.grid(row=1, column=0, sticky='n')
        self.log_type_combobox.grid(row=1, column=1, sticky='n')
        log_date_label = tkinter.Label(self.rootTk, text='log date:')
        log_date_label.grid(row=1, column=2, sticky='n')
        self.log_date_entry.grid(row=1, column=3, sticky='n')
        log_filter_label = tkinter.Label(self.rootTk, text=LogsDownload.logFilterKey + ':')
        log_filter_label.grid(row=2, column=0, sticky='n')
        self.log_filter_entry.grid(row=2, column=1, sticky='n')
        self.download_button.grid(row=3, column=0, sticky='n', padx=10)
        self.logs_to_postman_button.grid(row=3, column=1, sticky='n', padx=10)
        # 加载服务列表
        self.get_server_service()
        # 加载服务器列表
        self.get_server_list()
        # 加载日志类型列表
        self.get_log_type_list()
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

    def get_log_type_list(self):
        """加载日志类型列表"""
        log_type_list = list(LogsDownload.logTypeConfig.keys())
        self.log_type_combobox['values'] = log_type_list
        self.log_type_combobox.current(0)
        self.log_type_combobox.update()

    def get_log_type(self):
        """获取日志类型"""
        log_type = self.log_type_combobox['values'][self.log_type_combobox.current()]
        return log_type

    def get_server_ip(self):
        """获取服务器ip"""
        server_str = self.server_list_combobox['values'][self.server_list_combobox.current()]
        server_info = server_str.split(' ')
        return server_info[0]

    def get_date_list(self):
        """获取日期范围"""
        log_date_str = str(self.log_date_entry.get())
        log_date_str = log_date_str.replace("\n", ',')
        log_date_str = log_date_str.replace("-", '')
        log_date_str = log_date_str.replace("/", '')
        log_date_str = log_date_str.replace("\\", '')
        log_date_str = log_date_str.replace(".", '')
        if log_date_str:
            date_list = log_date_str.split(',')
        else:
            date_list = [time.strftime('%Y%m%d', time.localtime(time.time()))]
        return date_list

    def logs_download(self):
        """下载日志文件"""
        server_type_list = []
        if self.server_online_value.get():
            server_type_list.append('online')
        if self.server_test_value.get():
            server_type_list.append('test')
        if self.server_dev_value.get():
            server_type_list.append('dev')
        server_ip_list = []
        if len(server_type_list) > 0:
            service_str = self.service_combobox['values'][self.service_combobox.current()]
            server_config_list = get_server_by_service(service_str)
            for service in server_config_list.keys():
                server_list = server_config_list[service]
                if server_list:
                    for server in server_list:
                        server_config = server_list[server]
                        if 'server_type' in server_config.keys() and server_config['server_type'] in server_type_list:
                            server_ip_list.append(server)
        else:
            server_ip_list.append(self.get_server_ip())
        for ip in server_ip_list:
            self.download_log_from_server(ip)

    def download_log_from_server(self, ip):
        log_type = self.get_log_type()
        log_config = LogsDownload.logTypeConfig[log_type]
        # 下载文件
        log_file_name = log_config['log_file_name']
        date_list = self.get_date_list()
        log_path = '/export/mba/logs/'
        if 'prestoRequest' == log_type:
            log_path = '/export/gdata/logs/'
        if 'javaMonitorRequest' == log_type:
            log_path = '/export/Logs/java_monitor/'
        download_file_info_list = []
        for log_date in date_list:
            log_file_path = LogsDownload.logFileDownloadPath + ip + '/' + log_date + "/"
            download_file = log_path + log_date + '/' + log_file_name
            if 'prestoRequest' == log_type:
                if log_date == time.strftime('%Y%m%d', time.localtime(time.time())):
                    download_file = log_path + log_file_name
                else:
                    log_date = datetime.datetime.strptime(log_date, '%Y%m%d')
                    log_date = log_date.strftime('%Y-%m-%d')
                    download_file = log_path + log_file_name + '_' + log_date + '.log'
            save_file = log_file_path + log_file_name
            download_file_info_list.append({
                'download_file': download_file,
                'save_file': save_file
            })
        SSH.ssh_server(ip)
        SSH.down_files(download_file_info_list)
        for download_file_info in download_file_info_list:
            self.current_download_log_file_path = download_file_info['save_file']
            # 将日志同步到数据库
            self.logs_to_db(ip)
        # 关闭终端
        # SSH.close()

    def logs_to_db(self, server_ip=None):
        """同步日志到数据库"""
        log_config = LogsDownload.logTypeConfig[self.get_log_type()]
        php_file_path = log_config['save_to_db_script']
        server_ip = server_ip if server_ip is not None else self.get_server_ip()
        command_info = [
            get_env_config('php', 'php'),
            php_file_path,
            self.current_download_log_file_path,
            server_ip,
        ]
        command_str = ' '.join(command_info)
        os.system(command_str)

    def logs_to_postman(self):
        """日志转成postman的形式"""
        filter_str = str(self.log_filter_entry.get())
        filter_str = filter_str.replace("\n", ',')
        log_config = LogsDownload.logTypeConfig[self.get_log_type()]
        php_file_path = log_config['log_to_postman_script']
        command_info = [
            get_env_config('php', 'php'),
            php_file_path,
            filter_str,
        ]
        command_str = ' '.join(command_info)
        os.system(command_str)

    def show(self):
        """显示日志下载界面"""
        self.show_download()
