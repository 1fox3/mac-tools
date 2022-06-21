#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from datetime import datetime, timedelta
import tkinter
from tkinter import ttk

from package.gui.workTools.gEDb.GEDbLogin import GEDbLogin
from package.gui.workTools.gEDb.GEDbTableRsync import GEDbTableRsync
from package.tools.SSH.SSH import SSH
from package.config.GEDb import get_login_command
from package.tools.JD.GE.GEFileData import GEFileData


class GEDbTableDataDownload(GEDbTableRsync):
    """下载数据文件"""
    # 下载数据日期类型
    dateType = {
        '昨天': 'yesterday',
        '前天': 'before yesterday',
        '全部': 'total',
        '自定义': 'by range',
    }

    def __init__(self, root_tk):
        """首页初始化"""
        super().__init__(root_tk)
        # 下载数据日期类型
        self.date_type_combobox = ttk.Combobox(self.rootTk, width=10)
        self.date_range_entry = tkinter.Entry(self.rootTk, width=50)
        self.extra_where_entry = tkinter.Entry(self.rootTk, width=50)
        # 下载按钮
        self.download_button = tkinter.Button(self.rootTk, command=self.download, text='download')

    def show_download(self):
        """服务器登录页面"""
        super().show()
        # 初始化界面
        date_type_label = tkinter.Label(self.rootTk, text='date type:', padx=10)
        date_type_label.grid(row=2, column=0, sticky='n')
        self.date_type_combobox.grid(row=2, column=1, sticky='n')
        date_range_label = tkinter.Label(self.rootTk, text='date range:', padx=10)
        date_range_label.grid(row=2, column=2, sticky='n')
        self.date_range_entry.grid(row=2, column=3, columnspan=3,  sticky='n')
        extra_where_label = tkinter.Label(self.rootTk, text='extra where:', padx=10)
        extra_where_label.grid(row=3, column=0, sticky='n')
        self.extra_where_entry.grid(row=3, column=1, columnspan=3, sticky='n')
        self.download_button.grid(row=1, column=4, sticky='s', ipadx=10)
        self.date_type_combobox['values'] = list(GEDbTableDataDownload.dateType.keys())
        self.date_type_combobox.current(0)
        self.date_type_combobox.update()
        self.rootTk.pack()

    def get_data_file_path(self):
        """获取文件存放路径"""
        table = self.get_table()
        return GEDbTableRsync.dataSavePath + table + '.txt'

    def get_data_file_save_path(self):
        """获取文件存放路径"""
        table = self.get_table()
        return GEDbTableRsync.dataDownloadPath + table + '.txt'

    def get_date_type(self):
        """获取当前数据类型"""
        data_type = self.date_type_combobox['values'][self.date_type_combobox.current()]
        return GEDbTableDataDownload.dateType[data_type]

    def get_data_date_range(self):
        """获取日期范围"""
        date_type = self.get_date_type()
        date_range = ''
        if 'yesterday' == date_type:
            date_range = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        if 'before yesterday' == date_type:
            date_range = (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d')
        if 'by range' == date_type:
            date_range_str = str(self.date_range_entry.get())
            date_range = list(date_range_str.split(','))
        return date_range

    def get_data_sql(self):
        """获取查询数据的sql"""
        sql = "select * from " + self.get_table()
        date_range = self.get_data_date_range()
        if isinstance(date_range, str) and date_range:
            sql += " where dt = '" + date_range + "'"
        if isinstance(date_range, list) and date_range:
            if 1 == len(date_range):
                sql += " where dt = '" + date_range.pop() + "'"
            else:
                date_str = "','".join(date_range)
                sql += " where dt in ('" + date_str + "')"
        extra_where = str(self.extra_where_entry.get())
        if len(extra_where) > 0:
            sql += ' and ' + extra_where
        return sql

    def create_data_file_command(self):
        """创建表列表文件"""
        db_config = self.login_db_config()
        login_command = get_login_command(db_config)
        login_command = login_command.replace(';', '')
        use_db_sql = 'use ' + db_config['db']
        set_charset_sql = 'set charset utf8'
        create_table_sql = "show create table " + self.get_table()
        data_sql = self.get_data_sql()
        file_path = self.get_data_file_path()
        return '%s -e "%s; %s; %s; %s;"  > %s' % (login_command, use_db_sql, set_charset_sql, create_table_sql,
                                                  data_sql, file_path)

    def save_table_data(self):
        """保存数据库表列表"""
        params = {
            'db_config': self.login_db_config(),
            'table': self.get_table(),
            'data_file_path': self.get_data_file_save_path(),
        }
        ge_file_data_obj = GEFileData(**params)
        ge_file_data_obj.handle_data()

    def download(self):
        """登录服务器"""
        ip = GEDbLogin.loginServerIp
        SSH.ssh_server(ip)
        file_path = self.get_data_file_path()
        sql_command = self.create_data_file_command()
        date_range = self.get_data_date_range()
        sql_sleep_time = 5 * len(date_range) if isinstance(date_range, list) else 5
        commands = {
            "rm " + file_path: 1,
            sql_command: sql_sleep_time,
        }
        SSH.handle_command(commands)
        save_path = self.get_data_file_save_path()
        SSH.down_files(
            [
                {
                    'download_file': file_path,
                    'save_file': save_path,
                }
            ]
        )
        # SSH.close()
        self.save_table_data()

    def show(self):
        """显示日志下载界面"""
        self.show_download()
