#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import tkinter
import json

from package.gui.workTools.BaseGui import BaseGui


class StringHandle(BaseGui):
    """常用的字符串处理"""

    def __init__(self, root_tk):
        """首页初始化"""
        super(StringHandle, self).__init__(root_tk)
        # 文本域
        self.ori_text_area = tkinter.Text(self.rootTk)
        self.des_text_area = tkinter.Text(self.rootTk)
        # 文件上线处理按钮
        online_file_button_params = {
            'command': self.online_file_handle,
            'text': 'online file'
        }
        self.online_file_button = tkinter.Button(self.rootTk, **online_file_button_params)
        # 字符串转postman参数形式
        str_to_postman_button_param = {
            'command': self.str_to_postman_param_handle,
            'text': 'array print str to postman param'
        }
        self.str_to_postman_param_button = tkinter.Button(self.rootTk, **str_to_postman_button_param)
        # 字符串unicode解码
        unicode_decode_button_param = {
            'command': self.unicode_decode_handle,
            'text': 'unicode decode'
        }
        self.unicode_decode_button = tkinter.Button(self.rootTk, **unicode_decode_button_param)
        # 安卓日志整理
        android_log_button_param = {
            'command': self.android_log_handle,
            'text': 'android log'
        }
        self.android_log_button = tkinter.Button(self.rootTk, **android_log_button_param)
        # JSON转PostMan参数
        json_postman_param = {
            'command': self.json_postman_param_handle,
            'text': 'json to postman param'
        }
        self.json_postman_param_button = tkinter.Button(self.rootTk, **json_postman_param)
        # 统一服务接口参数增加clzType
        union_param_add_clz_type = {
            'command': self.union_param_add_clz_type_handle,
            'text': 'union param add clzType'
        }
        self.union_param_add_clz_type_button = tkinter.Button(self.rootTk, **union_param_add_clz_type)
        # EZD统一服务接口参数提取
        ezd_union_param = {
            'command': self.ezd_union_param_handle,
            'text': 'ezd union param'
        }
        self.ezd_union_param_button = tkinter.Button(self.rootTk, **ezd_union_param)

    def show_string_handle(self):
        """常用的字符串处理页面"""
        self.rootTk.pack()
        self.ori_text_area.grid(row=0, column=0, sticky='n')
        arrow_label = tkinter.Label(self.rootTk, text='->')
        arrow_label.grid(row=0, column=1, sticky='n')
        self.des_text_area.grid(row=0, column=2, sticky='n')
        self.online_file_button.grid(row=1, column=0, sticky='s', ipadx=10)
        self.str_to_postman_param_button.grid(row=1, column=2, sticky='s', ipadx=10)
        self.unicode_decode_button.grid(row=2, column=0, sticky='s', ipadx=10)
        self.android_log_button.grid(row=2, column=2, sticky='s', ipadx=10)
        self.json_postman_param_button.grid(row=3, column=0, sticky='s', ipadx=10)
        self.union_param_add_clz_type_button.grid(row=3, column=2, sticky='s', ipadx=10)
        self.ezd_union_param_button.grid(row=4, column=0, sticky='s', ipadx=10)

    def get_ori_string(self, split=False):
        """获取需要处理的字符串"""
        text_content = self.ori_text_area.get(0.0, tkinter.END)
        text_content = str.strip(text_content)
        return text_content if not split else text_content.split("\n")

    def write_des_string(self, des_str):
        """返回用户需要的字符串"""
        self.des_text_area.delete(0.0, tkinter.END)
        self.des_text_area.insert(0.0, des_str)

    def online_file_handle(self):
        """文件上线字符串处理"""
        files = self.get_ori_string(True)
        str_arr = []
        for file in files:
            if not file:
                continue
            file = file.replace('\\', '/')
            str_arr.append('/export/App/' + file)
        self.write_des_string("\n".join(str_arr))

    def str_to_postman_param_handle(self):
        """数组打印结果转postman参数字符串"""
        param_str = self.get_ori_string()
        replace_dict = {
            '] =>': ':',
            '[': '',
            ' ': '',
        }
        self.write_des_string(StringHandle.str_multi_replace(param_str, replace_dict))

    def unicode_decode_handle(self):
        """unicode编码解码"""
        param_str = self.get_ori_string()
        self.write_des_string(param_str.encode('utf8').decode('unicode_escape'))

    @staticmethod
    def str_multi_replace(ori_str, replace_dict):
        """字符串多重替换"""
        if not isinstance(ori_str, str) or not isinstance(replace_dict, dict):
            return ''
        for old, new in replace_dict.items():
            ori_str = ori_str.replace(old, new)
        return ori_str

    def android_log_handle(self):
        """安卓日志处理"""
        param_str_list = self.get_ori_string(True)
        final_str = ''
        for param_str in param_str_list:
            start_pos = 0
            for i in range(4):
                start_pos = param_str.find(' ', start_pos + 1)
                if -1 == start_pos:
                    break
            if -1 != start_pos:
                param_str = param_str[start_pos + 1:]
                param_str.strip()
                final_str += param_str
        json_start_pos = final_str.find('{')
        final_str = final_str[json_start_pos:]
        json_end_pos = final_str.rfind('}')
        final_str = final_str[0:json_end_pos + 1]
        self.write_des_string(final_str)

    def json_postman_param_handle(self):
        """json转postman参数"""
        param_str = self.get_ori_string()
        param_dict = json.loads(param_str)
        final_str = ''
        for key in param_dict:
            val = param_dict[key]
            if val is None:
                val = ''
            final_str += str(key) + ':' + str(val) + "\n"
        self.write_des_string(final_str)

    def union_param_add_clz_type_handle(self):
        """统一服务接口参数增加clzType"""
        param_str = self.get_ori_string()
        param_dict = json.loads(param_str)
        key_list = ['body', 'criteria', 'criterions']
        param = param_dict
        for key in key_list:
            param = param[key]
        if param is not None:
            for dim_param in param:
                cle_type = 'InExpression' if 'in' == dim_param['op'] else 'SimpleExpression'
                dim_param['clzType'] = cle_type

        order_key_list = ['body', 'criteria', 'orders']
        order_param = param_dict
        for key in order_key_list:
            order_param = order_param[key]
        if 0 != len(order_param):
            order_param[0]['clzType'] = 'UOrder'

        self.write_des_string(json.dumps(param_dict))

    def ezd_union_param_handle(self):
        """EZD统一服务接口参数提取"""
        param_str = self.get_ori_string()
        param_dict = json.loads(param_str)
        key_list = ['params', 'requestJson']
        param = param_dict
        for key in key_list:
            param = param[key]
        self.write_des_string(param)

    def show(self):
        """显示常用的字符串处理初始界面"""
        self.show_string_handle()
