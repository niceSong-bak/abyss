# -*- coding: utf-8 -*-
# @Time : 2019-06-28 11:28
# @Email : aaronlzxian@163.com
# @File : module_parser_test.py

import os
import unittest
from abyss.module_parser import ModuleParser

directory = os.path.join(os.path.dirname(os.path.abspath(__file__)) + os.path.sep + "..", 'build/build')
if not os.path.exists(directory):
    os.makedirs(directory)

class ModuleParserTest(unittest.TestCase):
    def setUp(self):
        self.module_parser = ModuleParser(directory)

    def test_modify_modules(self):
        # self.modules = self.module_parser.modify_modules(["y/build.gradle", 'x/build.gradle', 'z/src/main'])
        self.modules = self.module_parser.modify_modules(["src/views/pay/payOnline.vue", 'src/assets/css/index.css'])
        print(self.modules)
