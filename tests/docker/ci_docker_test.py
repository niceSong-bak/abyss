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
            "id":"67dbff5d38ea31c1de6abf0928dd1c8926bedd30",
            "tree_id":"7c2556e2d0aec5ca10db75f304551f490b49d84c",
            "parent_ids":[
                "feb1b8ec83084953612955e66800b5b2897e0968"
            ],
            "message":"妮玛为啥子不得行呢",
            "timestamp":"2019-08-23T15:09:58+08:00",
            "url":"https://gitee.com/jinuoimf/ProxyPool/commit/67dbff5d38ea31c1de6abf0928dd1c8926bedd30",
            "author":{
                "time":"2019-08-23T15:09:58+08:00",
                "id":1410931,
                "name":"aaron",
                "email":"aaronlzxian@163.com",
                "username":"nosir",
                "user_name":"nosir",
                "url":"https://gitee.com/nosir",
                "remark":"刘仲贤"
            },
            "committer":{
                "id":1410931,
                "name":"aaron",
                "email":"aaronlzxian@163.com",
                "username":"nosir",
                "user_name":"nosir",
                "url":"https://gitee.com/nosir",
                "remark":"刘仲贤"
            },
            "distinct":true,
            "added":[

            ],
            "removed":[

            ],
            "modified":[
                "src/main.js"
            ]
        }
    ]
'''


class TestBeta(unittest.TestCase):

    def test_tag(self):
        CIDocker(
            workplace=directory,
            git_url="git@gitee.com:jinuotech/igc-mainsite-frontend.git",
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
            pipe="prod"
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
