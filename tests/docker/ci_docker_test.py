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
            "id":"eda79f4d6555225f1614721e17b88b527b6746ca",
            "tree_id":"e951498f7ae1202bad095221ce7be025ae146f44",
            "parent_ids":[
                "75c9fc5b809bf524e0b49b8770dc60f634638a0c"
            ],
            "message":"style fix",
            "timestamp":"2019-07-10T10:02:28+08:00",
            "url":"https://gitee.com/twisted06/twisted2_web/commit/eda79f4d6555225f1614721e17b88b527b6746ca",
            "author":{
                "time":"2019-07-10T10:02:28+08:00",
                "name":"604801215@qq.com",
                "email":"qwer1234"
            },
            "committer":{
                "name":"604801215@qq.com",
                "email":"qwer1234"
            },
            "distinct":true,
            "added":[

            ],
            "removed":[

            ],
            "modified":[
                "src/assets/css/index.css",
                "src/views/pay/payOnline.vue"
            ]
        }
    ]
'''


class TestBeta(unittest.TestCase):

    def test_tag(self):
        CIDocker(
            workplace=directory,
            git_url="https://gitee.com/twisted06/twisted2_web.git",
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
