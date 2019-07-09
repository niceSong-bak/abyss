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


class TestBeta(unittest.TestCase):

    def test_tag(self):
        CIDocker(
            workplace=directory,
            # git_url="git@gitee.com:jinuotech/Tristana-AdminFrontend.git",
            # git_url="git@gitee.com:floozy/springdemo.git",
            # git_url="https://gitee.com/jinuotech/Paymire.git",
            git_url="https://gitee.com/twisted06/twisted2_web.git",
            git_ref="refs/tags/v1.2.6.3",
            pipe="beta"
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
