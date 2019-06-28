# -*- coding: utf-8 -*-
# @Time : 2019-06-28 11:04
# @Email : aaronlzxian@163.com
# @File : module_parser.py
import os
import re
from abyss import logger as LOG

ABYSSYAML = 'abyss.yaml'
pattern = re.compile('^(\d|\w)+?/')

class ModuleParser:
    def __init__(self, project_path):
        self.project_path = project_path
        self.g = os.walk(project_path)
        self.short_module_names = []

    def modify_modules(self, commits):
        LOG.big_log_start("Start parser module")
        result = set()
        modules = set()
        for path, dirs, file_names in self.g:
            #根目录全局打包
            if self.project_path == path:
                for file_name in file_names:
                    if file_name in commits:
                        LOG.debug(path)
                        result.add(path)
                        self.short_module_names.append('All')
                        return result
            if ABYSSYAML in file_names and path not in modules:
                modules.add(path)

        for commit in commits:
            module = pattern.findall(commit)[0]
            self.short_module_names.append(module)
            module_path = os.path.join(self.project_path, module)
            if module_path in modules and module_path not in result:
                LOG.debug(module_path)
                result.add(module_path)
        return result




