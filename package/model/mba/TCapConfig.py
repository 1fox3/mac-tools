#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from package.model.Model import Model
from package.config.GEServer import GEServer
from package.tools.Help.Str import Str


class TCapConfig(Model):
    """容器配置表"""
    # 主键
    mainKey = 'ip'

    def get_config_str(self):
        """将数据转成配置"""
        return Str.dict_to_config_str(self.get_all({'cap_status': 0}), TCapConfig.mainKey)

    def save_config_to_table(self):
        """将配置保存到数据表"""
        # 截断数据表
        self.truncate_table()
        return self.insert(GEServer.values())
