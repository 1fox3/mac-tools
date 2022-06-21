#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import pymysql
import time

from package.tools.Sql.MySql import MySql


class GEFileData:
    """ge数据库表"""

    def __init__(self, *args, **kwargs):
        """初始化参数"""
        self.db = ''
        self.replace_dict = {}
        args = kwargs.keys()
        if 'db_config' in args:
            self.db_config = kwargs['db_config']
            self.db = self.db_config['db']
        if 'table' in args:
            self.table = kwargs['table']
        if 'data_file_path' in args:
            self.data_file_path = kwargs['data_file_path']
        if 'replace_dict' in args:
            self.replace_dict = kwargs['replace_dict']
        if not self.db and 'db' in args:
            self.db = kwargs['db']
        self.data_file_resource = None
        self.data_keys = []

    def del_table(self):
        """删除数据表"""
        return MySql.connect(self.db).query("drop table " + self.table)

    def open_data_file(self):
        """打开数据文件"""
        if not self.data_file_resource and self.data_file_path:
            self.data_file_resource = open(self.data_file_path, 'r', encoding='utf-8')

    def handle_data(self):
        """处理数据"""
        start_time = time.time()
        self.open_data_file()
        rows_info = []
        while True:
            data_line = self.data_file_resource.readline()
            if not data_line:
                break
            data_line = str.strip(data_line)
            values = data_line.split('\t')
            if not self.data_keys:
                self.data_keys = values
                continue
            row_info = dict(zip(self.data_keys, values))
            if 'Create Table' in self.data_keys and 'Table' in self.data_keys:
                self.save_data(row_info)
            else:
                rows_info.append(row_info)
            if 300 <= len(rows_info):
                self.save_data(rows_info)
                rows_info.clear()
        if 0 < len(rows_info):
            self.save_data(rows_info)
        print(time.time() - start_time)

    def get_value_str(self, values):
        """拼接value字符串"""
        key_join = '\',\''
        value_list = []
        for value in values:
            value_list.append(pymysql.converters.escape_string(value))
        value_str = '(\'' + key_join.join(value_list) + '\')'
        if self.replace_dict:
            for old, new in self.replace_dict.items():
                value_str = value_str.replace(old, new)
        return value_str

    @staticmethod
    def get_key_str(values):
        """拼接value字符串"""
        key_join = '`,`'
        return '(`' + key_join.join(values) + '`)'

    def save_data(self, data):
        """保存数据"""
        key_str = GEFileData.get_key_str(self.data_keys)
        if 'Create Table' in self.data_keys and 'Table' in self.data_keys:
            sql = data['Create Table'].replace('\\n', '')
            drop_table_sql = 'DROP TABLE IF EXISTS ' + self.table
            try:
                # 删除表
                MySql.connect(self.db).query(drop_table_sql)
            except pymysql.err.Error as e:
                print(e)
                print(sql)
            try:
                # 重新创建表
                MySql.connect(self.db).query(sql)
            except pymysql.err.Error as e:
                print(e)
                print(sql)

            self.data_keys = None
        else:
            if isinstance(data, dict):
                value_list = [data]
            if isinstance(data, list):
                value_list = data
            value_str = []
            for value in value_list:
                value_str.append(self.get_value_str(value.values()))
            sql = r"INSERT INTO `%s`.`%s` %s VALUES %s" % (self.db, self.table, key_str, ','.join(value_str))
            # 处理数据为NULL的情况，防止转换成字符串NULL
            sql = sql.replace("'NULL'", "NULL")
            try:
                MySql.connect(self.db).query(sql)
            except pymysql.err.Error as e:
                print(e)
                print(sql)
