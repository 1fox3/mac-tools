#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
本地调试文件配置
"""
GECode = {
    'online_debug': {
        'file_save_path': '/Users/lusongsong/Code/php/onlineDebug',
        'files': {
            # 调试文件
            'Debug.php': '/export/App/mba_jd_com/version_path/common/lib/MBA/Core/',
            # 版本文件
            'CommonController.class.php': '/export/App/mba_jd_com/version_path/controller/',
            'TokenCheckApi.class.php': '/export/App/mba_jd_com/version_path/api/',
            'MBA.class.php': '/export/App/mba_jd_com/version_path/common/lib/MBA/Core/',
            'MBA_Curl.class.php': '/export/App/mba_jd_com/version_path/common/lib/MBA/Core/',
            'MBA_Db_Mysql.class.php': '/export/App/mba_jd_com/version_path/common/lib/MBA/Plugins/DbDriver/',
            'MBA_Db_ClickHouse.class.php': '/export/App/mba_jd_com/version_path/common/lib/MBA/Plugins/DbDriver/',
        }
    },
    # 主站代码默认版本
    'ge_ch_default_version': '4.3.7',
}
