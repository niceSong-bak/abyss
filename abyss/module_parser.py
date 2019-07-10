# -*- coding: utf-8 -*-
# @Time : 2019-06-28 11:04
# @Email : aaronlzxian@163.com
# @File : module_parser.py
import os
import re
from abyss import logger as LOG

ABYSSYAML = 'abyss.yaml'

class ModuleParser:
    def __init__(self, project_path):
        self.project_path = project_path
        self.g = os.walk(project_path)
        self.short_module_names = []

    def modify_modules(self, commits):
        LOG.big_log_start("Start parser module")
        result = set()

        #创建新分支
        if commits is None or len(commits) < 1:
            LOG.debug(self.project_path)
            result.add(self.project_path)
            return result

        self.modules = set()
        for path, dirs, file_names in self.g:
            #根目录全局打包


            if self.project_path == path:
                for file_name in file_names:
                    if file_name in commits:
                        LOG.debug(path)
                        result.add(path)
                        return result
            if ABYSSYAML in file_names and path not in self.modules:
                self.modules.add(path)

        for commit in commits:
            module_path = self.match_module(commit)
            LOG.debug(module_path)
            if module_path == self.project_path:
                result.add(module_path)
                return result
            if module_path not in result:
                result.add(module_path)
        return result

    def match_module(self, commit):
        result = self.project_path
        commit = self.project_path + '/' + commit
        for item in self.modules:
            if commit.startswith(item) and len(result) < len(item):
                result = item
        return result








