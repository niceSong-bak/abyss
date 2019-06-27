#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import unittest
import sys

from abyss.docker.ci_docker import CIDocker

directory = os.path.join(os.path.dirname(os.path.abspath(__file__)) + os.path.sep + "../..", 'build')
if not os.path.exists(directory):
    os.makedirs(directory)

commit_json = '''
[
        {
            "id":"db116c3ca946dd8d6fb4c4feeec7a88d4be8f835",
            "tree_id":"ee0d719f43001da96972f98f366dab172ef794b2",
            "parent_ids":[
                "9d3508a0d702514cebdf550e0f54e7752027adea"
            ],
            "message":"dd",
            "timestamp":"2019-06-28T11:33:45+08:00",
            "url":"https://gitee.com/floozy/springdemo/commit/db116c3ca946dd8d6fb4c4feeec7a88d4be8f835",
            "author":{
                "time":"2019-06-28T11:33:45+08:00",
                "id":1410931,
                "name":"nosir",
                "email":"aaronlzxian@163.com",
                "username":"nosir",
                "user_name":"nosir",
                "url":"https://gitee.com/nosir",
                "remark":"刘仲贤"
            },
            "committer":{
                "id":1410931,
                "name":"nosir",
                "email":"aaronlzxian@163.com",
                "username":"nosir",
                "user_name":"nosir",
                "url":"https://gitee.com/nosir",
                "remark":"刘仲贤"
            },
            "distinct":true,
            "added":[
                "z/src/main",
                "x/src/main"
            ],
            "removed":[
                "y/build.gradle",
                "x/build.gradle"
            ],
            "modified":[
                "z/build.gradle"
            ]
        }
    ]
'''


class TestBeta(unittest.TestCase):

    def test_tag(self):
        CIDocker(
            workplace=directory,
            # git_url="git@gitee.com:jinuotech/Tristana-AdminFrontend.git",
            # git_url="git@gitee.com:floozy/springdemo.git",
            git_url="https://gitee.com/jinuotech/Paymire.git",
            git_ref="refs/heads/dev",
            pipe="beta",
            commits=commit_json
        ).ci_process()


class TestProd(unittest.TestCase):

    def test_tag(self):
        if not CIDocker(
            workplace=directory,
            git_url="git@gitee.com:floozy/springdemo.git",
            git_ref="refs/heads/devww",
            pipe="release"
        ).ci_process():
            print("ssssss")
            sys.exit(1)
        print("ddddd")

    def test_version(self):
        version = re.sub('^v(?=\d+)', '', "v1.0.1")
        self.assertEqual('1.0.1', version)


class TestAws(unittest.TestCase):

    def test_tag(self):
        CIDocker(
            workplace=directory,
            git_url="git://gitee.com/twisted06/Twisted-WatcherService.git",
            git_ref="refs/tags/v1.2.4.4",
            pipe="prod"
        ).ci_process()


if __name__ == "__main__":
    unittest.main()
