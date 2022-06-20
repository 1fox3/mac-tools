#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import re
import time


class Git:
    """git相关操作"""

    @staticmethod
    def get_change_file_info(path):
        """查询文件修改列表"""
        try:
            original_path = os.getcwd()
            os.chdir(path)
            git_status = os.popen('git status')
            os.chdir(original_path)
            files = []
            for git_status_line in git_status:
                if git_status_line.startswith('\t'):
                    git_status_line = git_status_line.strip()
                    file_arr = git_status_line.split(':')
                    if 1 == len(file_arr):
                        file_arr.insert(0, 'added')
                    mode = file_arr[0]
                    file_path = file_arr[1].strip()
                    modify_time = 0
                    if 'deleted' != mode:
                        file_root_path = path + '/' + file_path
                        file_root_path = file_root_path.replace('\\', '/')
                        modify_time = os.path.getmtime(file_root_path)
                    file_info = {'mode': mode, 'file_path': file_path, 'file_m_time': modify_time}
                    files.append(file_info)
            files.sort(key=lambda x: (x['file_m_time']), reverse=True)
            for file_info in files:
                time_info = time.localtime(file_info['file_m_time'])
                file_info['file_m_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time_info)
        except IOError as e:  # 程序出错时运行
            print('git查询文件修改失败：' + e)
        git_status.close()
        return files

    @staticmethod
    def checkout_file(path, file_list):
        """取消版本库中代码文件的修改"""
        try:
            if isinstance(file_list, str):
                file_list = [file_list]
            if isinstance(file_list, list):
                original_path = os.getcwd()
                os.chdir(path)
                for file_path in file_list:
                    if isinstance(file_path, str):
                        git_cmd = os.popen('git checkout ' + file_path)
                        git_cmd.close()
                os.chdir(original_path)
        except IOError as e:  # 程序出错时运行
            print('git查询文件修改失败：' + e)
            return False
        return True

    @staticmethod
    def skip_worktree_file(path, file_list):
        """忽略本地文件"""
        try:
            if isinstance(file_list, str):
                file_list = [file_list]
            if isinstance(file_list, list):
                original_path = os.getcwd()
                os.chdir(path)
                for file_path in file_list:
                    if isinstance(file_path, str):
                        git_cmd = os.popen('git update-index --skip-worktree ' + file_path)
                        git_cmd.close()
                os.chdir(original_path)
        except IOError as e:  # 程序出错时运行
            print('git忽略本地文件失败：' + e)
            return False
        return True

    @staticmethod
    def no_skip_worktree_file(path, file_list):
        """取消忽略本地文件"""
        try:
            if isinstance(file_list, str):
                file_list = [file_list]
            if isinstance(file_list, list):
                original_path = os.getcwd()
                os.chdir(path)
                for file_path in file_list:
                    if isinstance(file_path, str):
                        git_cmd = os.popen('git update-index --no-skip-worktree ' + file_path)
                        git_cmd.close()
                os.chdir(original_path)
        except IOError as e:  # 程序出错时运行
            print('git取消忽略本地文件失败：' + e)
            return False
        return True


if __name__ == "__main__":
    info = Git.get_change_file_info('/Users/lusongsong/Code/python/mac-tools')
    print(info)
