#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from package.tools.Sql.MySql import MySql


class GEDbTable:
    """ge数据库表"""

    # 页面保存名称
    db = 'mba'
    table = 't_ge_db_table'

    @staticmethod
    def get_table_by_db(db_name):
        """查询表列表"""
        sql = "SELECT * FROM " + GEDbTable.table + " WHERE db = '" + db_name + "'"
        return MySql.connect(GEDbTable.db).query(sql)
