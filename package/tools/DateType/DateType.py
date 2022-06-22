#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import time
import requests
import traceback

from package.tools.Log.DBLog import DBLog
from package.model.admin.TWorkDateType import TWorkDateType


class DateType:
    """日期类型"""
    # 日期类型
    dateTypeEnum = (
        'workday',  # 工作日
        'holiday',  # 假期
        'transfer',  # 调班
        'weekend',  # 周末
        'unknown',  # 未知
    )

    @staticmethod
    def __get_date(date=''):
        """获取日期"""
        return time.strptime(date, '%Y-%m-%d') if date else time.localtime()

    @staticmethod
    def go_seek_date_type(date):
        """
        获取日期类型的接口
        反回数据样例：{"code":10000,"data":3}
        data解释：正常工作日对应结果为 0, 法定节假日对应结果为 1, 节假日调休补班对应的结果为 2，休息日对应结果为 3
        还有另外一个接口，接口文档：http://www.easybots.cn/holiday_api.net
        """
        date_type_param = {
            'date': time.strftime("%Y%m%d", date),
        }
        api = 'http://api.goseek.cn/Tools/holiday'
        # 调用接口
        # noinspection PyBroadException
        try:
            date_type_json_str = requests.get(api, date_type_param)
            date_type_json = date_type_json_str.json()
        except Exception as e:
            print(date_type_json_str)
            # 发生异常，默认给成功，工作日
            date_type_json = {
                'code': 10000,
                'data': 0
            }
        DBLog.log(**{
            'break_point': 'dateTypeApiRequest',
            'log_info': {
                'api': api,
                'params': date_type_param,
                'response': date_type_json,
            }
        })
        # 获取有效的日期类型
        date_type_enum_len = len(DateType.dateTypeEnum)
        date_type_num = date_type_enum_len - 1
        if isinstance(date_type_json, dict) and date_type_json and 'data' in date_type_json.keys():
            date_type_num = int(date_type_json['data'])
        if date_type_num < 0 or date_type_num >= date_type_enum_len:
            date_type_num = date_type_enum_len - 1
        return DateType.dateTypeEnum[date_type_num]

    @staticmethod
    def bitefu_date_type(date):
        """
        获取日期类型的接口
        反回数据样例：1
        data解释：正常工作日对应结果为 0, 休息日对应结果为 1, 法定节假日对应结果为 2
        还有另外一个接口，接口文档：http://www.easybots.cn/holiday_api.net
        """
        date_type_param = {
            'd': time.strftime("%Y%m%d", date),
        }
        api = 'http://tool.bitefu.net/jiari/'
        # 调用接口
        # noinspection PyBroadException
        try:
            date_type_json_str = requests.get(api, date_type_param)
            date_type_num = date_type_json_str.json()
        except Exception as e:
            DBLog.log(**{
                'break_point': 'dateTypeApiException',
                'log_info': {
                    'api': api,
                    'params': date_type_param,
                    'exception': e.__str__(),
                }
            })
            # 发生异常，默认给成功，工作日
            date_type_num = 0
        DBLog.log(**{
            'break_point': 'dateTypeApiRequest',
            'log_info': {
                'api': api,
                'params': date_type_param,
                'response': date_type_num,
            }
        })
        # 获取有效的日期类型
        if 2 == date_type_num:
            return DateType.dateTypeEnum[1]
        elif 1 == date_type_num:
            return DateType.dateTypeEnum[3]
        elif 0 == date_type_num:
            if DateType.is_weekend(time.strftime("%Y-%m-%d", date),):
                return DateType.dateTypeEnum[2]
            else:
                return DateType.dateTypeEnum[0]
        else:
            return DateType.dateTypeEnum[4]

    @staticmethod
    def get_date_type(date=''):
        """获取日期类型"""
        # 处理date参数
        date = DateType.__get_date(date)
        date_db_str = time.strftime("%Y-%m-%d", date)
        date_type_ret = None
        date_type_model = None
        # noinspection PyBroadException
        try:
            date_type_model = TWorkDateType()
            date_type_ret = date_type_model.get_one({'dt': date_db_str})
        except Exception as e:
            DBLog.log(**{
                'break_point': 'browserAutoWorkTimeSubmitException',
                'log_info': traceback.format_exc()
            })
        date_type = 'unknown'
        if date_type_ret and isinstance(date_type_ret, dict) and 'type' in date_type_ret.keys():
            date_type = date_type_ret['type']
        if 'unknown' != date_type:
            return date_type

        # 采用goseek获取日期类型
        # date_type = DateType.go_seek_date_type(date)
        # 采用bitefu获取日期类型
        date_type = DateType.bitefu_date_type(date)
        # noinspection PyBroadException
        try:
            if date_type_ret:
                date_type_model.update(
                    {'dt': date_db_str},
                    {'type': date_type}
                )
            else:
                date_type_model.insert({
                    'dt': date_db_str,
                    'type': date_type,
                })
        except Exception as e:
            DBLog.log(**{
                'break_point': 'browserAutoWorkTimeSubmitException',
                'log_info': traceback.format_exc()
            })
        return date_type

    @staticmethod
    def get_date_week_num(date=''):
        """
        获取日期的星期序号
        星期日：0
        星期一：1
        星期二：2
        星期三：3
        星期四：4
        星期五：5
        星期六：6
        """
        date = DateType.__get_date(date)
        return int(time.strftime('%w', date))

    @staticmethod
    def is_holiday(date=''):
        """判断日期是否为假期"""
        return 'holiday' == DateType.get_date_type(date)

    @staticmethod
    def is_work_day(date=''):
        """判断日期是否为法定工作日，包含普通工作日和调班"""
        return DateType.get_date_type(date) in ['workday', 'transfer']

    @staticmethod
    def is_rest_day(date=''):
        """判断日期是否为法定休息日，包含假期和周末"""
        return DateType.get_date_type(date) in ['holiday', 'weekend']

    @staticmethod
    def is_workday(date=''):
        """判断日期是否为工作日"""
        week_num = DateType.get_date_week_num(date)
        return 1 <= week_num <= 5

    @staticmethod
    def is_weekend(date=''):
        """判断日期是否为周末"""
        week_num = DateType.get_date_week_num(date)
        return week_num in [0, 6]
