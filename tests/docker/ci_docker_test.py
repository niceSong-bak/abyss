#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import unittest

from abyss.docker import ci_docker_beta, ci_docker_prod, ci_docker_aws

directory = os.path.join(os.path.dirname(os.path.abspath(__file__)) + os.path.sep + "../..", 'build')
if not os.path.exists(directory):
    os.makedirs(directory)


class TestBeta(unittest.TestCase):

    def test_tag(self):
        ci_docker_beta.progress(
            workplace=directory,
            git_url="git@gitee.com:floozy/springdemo.git",
            git_ref="refs/heads/master",
            pipe="docker_beta"
        )


class TestProd(unittest.TestCase):

    def test_tag(self):
        ci_docker_prod.progress(
            workplace=directory,
            git_url="git@gitee.com:floozy/springdemo.git",
            git_ref="refs/tags/v2.0.42",
            pipe="docker_beta"
        )

    def test_version(self):
        version = re.sub('^v(?=\d+)', '', "v1.0.1")
        self.assertEqual('1.0.1', version)


class TestAws(unittest.TestCase):

    def test_tag(self):
        ci_docker_aws.progress(
            workplace=directory,
            git_url="git@gitee.com:floozy/springdemo.git",
            git_ref="refs/tags/v2.0.42",
            pipe="docker_beta"
        )


if __name__ == "__main__":
    unittest.main()
