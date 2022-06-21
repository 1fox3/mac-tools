#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import tkinter
from tkinter import ttk

from package.gui.workTools.gEDb.GEDbLogin import GEDbLogin
from package.tools.SSH.SSH import SSH
from package.tools.JD.GE.GEDbTable import GEDbTable
from package.config.GEDb import get_login_command
from package.model.mba.TGeDbTable import TGeDbTable
from package.tools.Help.File import File


class GEDbTableRsync(GEDbLogin):
    """同步数据表列表"""
    # 默认文件存放路径
    dataSavePath = '/tmp/'
    dataDownloadPath = '/Users/lusongsong/Downloads/'
    db = 'mba'
    table = 't_ge_db_table'

    def __init__(self, root_tk):
        """首页初始化"""
        super().__init__(root_tk)
        # 数据表
        self.table_combobox = ttk.Combobox(self.rootTk, width=30, postcommand=self.get_table_list)
        # 同步按钮
        self.rsync_button = tkinter.Button(self.rootTk, command=self.rsync, text='table rsync')

    def show_rsync(self):
        """数据表同步页面"""
        super().show()
        # 初始化界面
        table_label = tkinter.Label(self.rootTk, text='tables:', padx=10)
        table_label.grid(row=0, column=8, sticky='n')
        self.table_combobox.grid(row=0, column=9, sticky='n')
        self.rsync_button.grid(row=1, column=2, sticky='s', ipadx=10)
        # 加载数据表列表
        self.get_table_list()
        self.rootTk.update()

    def get_table_list(self):
        """根据数据库获取数据列表"""
        db_name = self.get_db_name()
        table_rows = GEDbTable.get_table_by_db(db_name)
        if table_rows:
            table_list = []
            for table_row in table_rows:
                if 'tb' in table_row.keys():
                    table_list.append(table_row['tb'])
            self.table_combobox['values'] = table_list
            self.table_combobox.current(0)
            self.table_combobox.update()
        else:
            self.table_combobox['values'] = []
            self.table_combobox.update()

    def get_table_file_path(self):
        """获取文件存放路径"""
        db_config = self.login_db_config()
        return GEDbTableRsync.dataSavePath + db_config['db_name'] + '.txt'

    def get_table_file_save_path(self):
        """获取文件存放路径"""
        db_config = self.login_db_config()
        return GEDbTableRsync.dataDownloadPath + db_config['db_name'] + '.txt'

    def create_table_file_command(self):
        """创建表列表文件"""
        db_config = self.login_db_config()
        login_command = get_login_command(db_config)
        login_command = login_command.replace(';', '')
        sql = "show tables;"
        file_path = self.get_table_file_path()
        return '%s -e "set charset utf8; use %s; %s"  > %s' % (login_command, db_config['db'], sql, file_path)

    def save_db_table(self):
        """保存数据库表列表"""
        db_model = TGeDbTable()
        db_config = self.login_db_config()
        file_obj = File().open(self.get_table_file_save_path(), 'r')
        tables = file_obj.readlines()
        for i in range(len(tables)):
            if 0 == i:
                continue
            db_model.insert({'db': db_config['db_name'], 'tb': tables[i].strip()})

    def get_table(self):
        """获取当前数据表名"""
        return self.table_combobox['values'][self.table_combobox.current()]

    def clear_table(self):
        """删除之前记录"""
        db_model = TGeDbTable()
        db_config = self.login_db_config()
        db_model.delete({'db': db_config['db_name']})

    def rsync(self):
        """同步数据表"""
        ip = GEDbLogin.loginServerIp
        SSH.ssh_server(ip)
        file_path = self.get_table_file_path()
        sql_command = self.create_table_file_command()
        commands = {
            "rm " + file_path: 1,
            sql_command: 5,
        }
        SSH.handle_command(commands)
        save_path = self.get_table_file_save_path()
        SSH.sz_file(file_path, save_path)
        # SSH.close()
        self.clear_table()
        self.save_db_table()

    def show(self):
        """显示日志下载界面"""
        self.show_rsync()
