#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from package.tools.Sql.MySql import MySql


class Model(MySql):
    def __init__(self):
        """首页初始化"""
        super().__init__()
        module_name = self.__class__.__module__
        class_info = module_name.split('.')
        class_name = class_info.pop()
        table = Model.get_db_or_table_from_class_name(class_name)
        class_name = class_info.pop()
        db = Model.get_db_or_table_from_class_name(class_name)
        self.db(db).table(table)

    @staticmethod
    def get_db_or_table_from_class_name(class_name):
        """根据类型获得数据库名或表名"""
        db_or_table_str = ''
        for i in range(len(class_name)):
            is_upper = class_name[i].isupper()
            is_digit = class_name[i].isdigit()
            if is_upper or is_digit:
                if 0 == i and is_upper:
                    db_or_table_str += class_name[i].lower()
                else:
                    db_or_table_str += '_'
                    if is_upper:
                        db_or_table_str += class_name[i].lower()
                    else:
                        db_or_table_str += class_name[i]
            else:
                db_or_table_str += class_name[i]
        return db_or_table_str
