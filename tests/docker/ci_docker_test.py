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
            "id":"7821c068153c4b77683490c40032d453fd80f248",
            "tree_id":"b0eada149d9637ceb719669fd0c74ec7c8840000",
            "parent_ids":[
                "29e665adf1dee649cdbfdd979033af2826033233"
            ],
            "message":"子目录abyss",
            "timestamp":"2019-08-19T14:56:06+08:00",
            "url":"https://gitee.com/jinuoimf/Gaia/commit/7821c068153c4b77683490c40032d453fd80f248",
            "author":{
                "time":"2019-08-19T14:56:06+08:00",
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
                "gaia-admin/abyss.yaml"
            ],
            "removed":[
            ],
            "modified":[
                "gaia-upms/src/main/kotlin/me/jinuo/imf/gaia/upms/controller/IndexController.kt"
            ]
        }
    ]
'''


class TestBeta(unittest.TestCase):

    def test_tag(self):
        CIDocker(
            workplace=directory,
            git_url="https://gitee.com/jinuoimf/Gaia.git",
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
