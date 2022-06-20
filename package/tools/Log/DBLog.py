#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import json

# from package.tools.Sql.MySql import MySql


class DBLog:
    """数据库存放日志"""
    db = 'mba'
    table = 't_log'

    @staticmethod
    def log(**log_param):
        """记录日志"""
        if not isinstance(log_param, dict) or not log_param:
            return False
        log_param_keys = log_param.keys()
        break_point = log_info = None
        if 'break_point' in log_param_keys:
            break_point = str(log_param['break_point'])
        if 'log_info' in log_param_keys:
            log_info = log_param['log_info']
        log_info = json.dumps(log_info)
        if not log_info:
            return False
        log_insert_sql = "INSERT INTO `%s`.`%s` (`break_point`, `log_info`) VALUES ('%s', '%s')" %\
                         (DBLog.db, DBLog.table, str(break_point), log_info.replace("'", "\\'"))
        print(log_insert_sql)
        # noinspection PyBroadException
        try:
            # return True if MySql.connect(DBLog.db).query(log_insert_sql) else False
            return True
        except Exception as e:
            pass
        return False
