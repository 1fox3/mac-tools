#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from package.model.Model import Model
from package.tools.Help.Str import Str
from package.config.GEDb import GEDb


class TGeDbConfig(Model):
    """数据库配置数据表"""

    def get_config_str(self):
        """将数据转成配置"""
        return Str.dict_to_config_str(self.get_all({}))

    def save_config_to_table(self):
        """将配置保存到数据表"""
        # 截断数据表
        self.truncate_table()
        return self.insert(GEDb)
