#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import pymysql
import re

from package.config.MySql import MySqlConfig
from package.config.CodeMsg import CodeMsg


class MySql:

    # 实例
    instance = None

    def __init__(self):
        """实例初始化"""
        # 错误信息集
        self.code_msg = CodeMsg['mysql']

        # 属性相关设置方法
        self.sql_key_fun = {
            'select': self.select,
            'where': self.where,
            'group by': self.group_by,
            'order by': self.order_by,
            'limit': self.limit,
        }

        # 数据库相关属性
        self.sql_db = None
        self.sql_table = None
        self.db_config = None
        self.db_conn = None
        self.db_cursor = None

        # sql相关属性
        self.sql_type = None
        self.sql_select = '*'
        self.sql_where = None
        self.sql_group_by = None
        self.sql_order_by = None
        self.sql_limit = None
        self.last_sql = None

        # 是否开启事务
        self.transaction = False

        # 查询结果相关属性
        self.code = None
        self.msg = None
        self.data = None
        # 插入id
        self.insert_id = None
        # 影响行数
        self.affected_rows = None

    def reset(self):
        """重置属性"""
        self.sql_select = '*'
        self.sql_where = None
        self.sql_group_by = None
        self.sql_order_by = None
        self.sql_limit = None
        self.last_sql = None

        self.code = None
        self.msg = None
        self.data = None

        self.insert_id = None
        self.affected_rows = None

    @staticmethod
    def get_instance():
        if MySql.instance is None:
            MySql.instance = MySql()
        return MySql.instance

    @staticmethod
    def connect(db):
        obj = MySql.get_instance()
        obj.db(db)
        return obj

    @staticmethod
    def handle_key_str(key_str):
        """处理key值"""
        return '`' + str(key_str) + '`'

    @staticmethod
    def handle_value_str(value_str):
        """处理value值"""
        return "'" + str(value_str) + "'"

    def get_db_conn(self):
        """获取数据库连接"""
        if not self.db_conn:
            # 数据库配置为空时，返回空
            if not self.db_config:
                return self.set_code_msg(10001)

            # 连接数据库
            try:
                self.db_conn = pymysql.connect(**self.db_config)
            except pymysql.err.InternalError as e:
                err_code = e.args[0]
                err_msg = e.args[1]
                self.db_conn = self.set_code_msg(err_code, None, err_msg)
        return self.db_conn

    def close_db_conn(self):
        """关闭数据库连接"""
        if self.db_conn:
            self.db_conn.close()
            self.db_conn = None

    def get_db_cursor(self):
        """获取数据库游标"""
        db_conn = self.get_db_conn()
        if db_conn:
            try:
                self.db_cursor = db_conn.cursor(pymysql.cursors.DictCursor)
            except pymysql.err.InternalError as e:
                err_code = e.args[0]
                err_msg = e.args[1]
                self.db_cursor = self.set_code_msg(err_code, None, err_msg)
        return self.db_cursor

    def close_db_cursor(self):
        """关闭数据库游标"""
        if self.db_cursor:
            self.db_cursor.close()
            self.db_cursor = None

    def start_transaction(self):
        """开启事务"""
        self.transaction = True

    def commit(self):
        """确认提交事务"""
        self.db_conn.commit()
        self.close_db_cursor()
        self.close_db_conn()
        self.transaction = False

    def rollback(self):
        """事务回滚"""
        self.db_conn.rollback()
        self.close_db_cursor()
        self.close_db_conn()
        self.transaction = False

    def query(self, sql):
        """执行sql"""
        self.reset()
        # 记录本次自行的sql
        self.last_sql = sql
        # 使用cursor()方法创建一个游标对象
        cursor = self.get_db_cursor()
        if not cursor:
            return None
        try:
            # 使用execute()方法执行SQL语句
            cursor.execute(str(sql))
            # 获取全部数据
            data = cursor.fetchall()
            data = self.set_code_msg(0, data)
            # 影响行数
            self.affected_rows = cursor.rowcount
            # 插入id
            if 'INSERT' == self.sql_type:
                self.insert_id = cursor.lastrowid
        except pymysql.err.InternalError as e:
            err_code = e.args[0]
            err_msg = e.args[1]
            data = self.set_code_msg(err_code, None, err_msg)

        # 关闭游标和数据库的连接
        if not self.transaction:
            self.commit()
        else:
            self.close_db_cursor()
        return data

    def db(self, db):
        """选择数据库"""
        self.sql_db = None
        if isinstance(db, str) and db in MySqlConfig.keys():
            self.sql_db = db
            db_config = MySqlConfig[self.sql_db]
            # 判断数据库配置是否完整
            config_keys = ['host', 'user', 'password', 'database']
            for config_key in config_keys:
                if config_key not in db_config.keys():
                    return self
            self.db_config = db_config
        else:
            print('缺少数据库配置' + db)

        return self

    def table(self, table):
        """选择数据表"""
        self.sql_table = None
        if isinstance(table, str):
            self.sql_table = table
        return self

    def get_table(self):
        """获取数据表"""
        return '`' + '`.`'.join([self.sql_db, self.sql_table]) + '`'

    def get_from(self):
        """获取from"""
        return 'FROM ' + self.get_table()

    def select(self, select):
        """设置数据取值范围"""
        self.sql_select = '*'
        select_list = []
        if isinstance(select, dict):
            for select_key, select_value in select.items():
                select_list.append(str(select_key) + ' AS ' + str(select_value))
        elif isinstance(select, str):
            select_list.append(select)
        else:
            select_list = list(select)
        if select_list:
            self.sql_select = ','.join(select_list)
        return self

    def get_select(self):
        """拼接select"""
        return 'SELECT ' + self.sql_select if self.sql_select else None

    def where(self, where):
        """设置数据查询范围"""
        self.sql_where = ''
        if isinstance(where, dict):
            where_list = []
            for where_key, where_value in where.items():
                sub_where = ''
                # 是否使用正则相关
                is_re = False
                if -1 == where_key.find(' '):
                    where_key = MySql.handle_key_str(where_key)
                    sub_where += where_key + ' = '
                else:
                    sub_where += where_key + ' '
                    if str(where_key).lower().find(' like'):
                        is_re = True
                if isinstance(where_value, list):
                    where_value = list(where_value)
                    sub_where += '('
                    for i in range(len(where_value)):
                        sub_where_value = where_value[i]
                        where_value[i] = re.escape(MySql.handle_value_str(sub_where_value))
                    sub_where += ', '.join(where_value)
                    sub_where += ')'
                else:
                    sub_where += "'" + re.escape(str(where_value)) + "'"
                if is_re:
                    sub_where = sub_where.replace('\\', '\\\\')
                where_list.append(sub_where)
            self.sql_where = ' AND '.join(where_list)
        else:
            self.sql_where = str(where)
        return self

    def get_where(self):
        """拼接where"""
        return 'WHERE ' + self.sql_where if self.sql_where else None

    def group_by(self, group_by):
        """设置数据分组设置"""
        self.sql_group_by = ''
        if isinstance(group_by, str):
            self.sql_group_by = group_by
        else:
            self.sql_group_by = ','.join(list(group_by))
        return self

    def get_group_by(self):
        """拼接group by"""
        return 'GROUP BY ' + self.sql_group_by if self.sql_group_by else None

    def order_by(self, order_by):
        """设置数据排序设置"""
        self.sql_order_by = ''
        order_by_list = []
        if isinstance(order_by, dict):
            for order_by_key, order_by_value in order_by.items():
                order_by_list.append(order_by_key + ' ' + order_by_value)
        elif isinstance(order_by, str):
            order_by_list.append(order_by)
        else:
            order_by_list = list(order_by)
        if order_by_list:
            self.sql_order_by = ','.join(order_by_list)
        return self

    def get_order_by(self):
        """拼接order by"""
        return 'ORDER BY ' + self.sql_order_by if self.sql_order_by else None

    def limit(self, limit):
        """设置数据条数设置"""
        self.sql_limit = ''
        if isinstance(limit, list):
            limit = list(limit)
            if 1 <= len(limit):
                limit_list = [str(int(limit[0]))]
                if 2 <= len(limit):
                    limit_list.append(str(int(limit[1])))
                self.sql_limit = ','.join(limit_list)
        else:
            self.sql_limit = str(limit)
        return self

    def get_limit(self):
        """拼接limit"""
        return 'LIMIT ' + self.sql_limit if self.sql_limit else None

    def get_all(self, where, sql_info={}):
        """查询记录"""
        self.where(where)
        if isinstance(sql_info, dict) and sql_info:
            sql_fun_keys = self.sql_key_fun.keys()
            for sql_key in sql_info.keys():
                if sql_key in sql_fun_keys:
                    self.sql_key_fun[sql_key](sql_info[sql_key])
        self.sql_type = 'SELECT'
        sql = ' '.join(filter(None, [
            self.get_select(),
            self.get_from(),
            self.get_where(),
            self.get_group_by(),
            self.get_order_by(),
            self.get_limit(),
        ]))
        data = self.query(sql)
        if 0 == self.get_code_msg()[0]:
            return data
        return None

    def get_one(self, where, sql_info={}):
        """查询单条记录"""
        sql_info['limit'] = 1
        data = self.get_all(where, sql_info)
        if data:
            return data[0]
        return {}

    def insert(self, info):
        """插入数据"""
        if not info:
            return self.set_code_msg(10002)
        key_str = ''
        if isinstance(info, dict):
            info = [info]
        info = list(info)
        values_list = []
        for i in range(len(info)):
            sub_info = info[i]
            if not sub_info:
                continue
            if isinstance(sub_info, dict):
                if not key_str:
                    key_list = []
                    for key in sub_info.keys():
                        key_list.append(MySql.handle_key_str(key))
                    key_str = '(' + ','.join(key_list) + ')'
                value_list = []
                for value in sub_info.values():
                    value_list.append(re.escape(MySql.handle_value_str(value)))
                values_list.append('(' + ','.join(value_list) + ')')
        self.sql_type = 'INSERT'
        sql = ' '.join([
            'INSERT INTO',
            self.get_table(),
            key_str,
            'VALUES',
            ','.join(values_list)
        ])
        self.query(sql)
        if 0 == self.get_code_msg()[0] and self.get_affected_rows():
            return self.get_insert_id()
        return False

    def update(self, where, update):
        """更新数据"""
        self.where(where)
        update_str = ''
        if isinstance(update, dict):
            update_list = []
            for update_key, update_value in update.items():
                update_list.append(MySql.handle_key_str(update_key) + ' = ' + MySql.handle_value_str(update_value))
            update_str += ','.join(update_list)
        self.sql_type = 'UPDATE'
        sql = ' '.join([
            'UPDATE',
            self.get_table(),
            'SET',
            update_str,
            self.get_where()
        ])
        self.query(sql)
        if 0 == self.get_code_msg()[0]:
            return True
        return False

    def delete(self, where):
        """删除数据"""
        self.where(where)
        self.sql_type = 'DELETE'
        sql = ' '.join([
            'DELETE',
            self.get_from(),
            self.get_where()
        ])
        data = self.query(sql)
        if 0 == self.get_code_msg()[0] and data:
            return True
        return False

    def set_code_msg(self, code, data=None, msg=None):
        """设置错误信息和数据"""
        self.code = int(code)
        self.data = data
        if msg:
            self.msg = msg
        else:
            if code in self.code_msg.keys():
                self.msg = self.code_msg[code]
        return data

    def get_insert_id(self):
        """获取插入id"""
        return self.insert_id

    def get_affected_rows(self):
        """获取影响行数"""
        return self.affected_rows

    def get_last_sql(self):
        """获取最近一次执行的sql"""
        return self.last_sql

    def get_code_msg(self):
        """获取错误信息"""
        return self.code, self.msg, self.data

    def get_create_table_sql(self):
        """获取表的创建语句"""
        create_table_sql = self.query('SHOW CREATE TABLE ' + self.get_table())
        if create_table_sql:
            return create_table_sql[0]['Create Table']
        return None

    def truncate_table(self, table=None):
        """截断数据表"""
        table = table if table else self.get_table()
        return self.query('TRUNCATE TABLE ' + table)

    def optimize_table(self, table=None):
        """整理数据表碎片"""
        table = table if table else self.get_table()
        return self.query('OPTIMIZE TABLE ' + table)
