#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import unittest

from abyss.docker import ci_docker_beta, ci_docker_prod

directory = os.path.join(os.path.dirname(os.path.abspath(__file__)) + os.path.sep + "../..", 'build')
if not os.path.exists(directory):
    os.makedirs(directory)


class TestBeta(unittest.TestCase):

    def test_tag(self):
        ci_docker_beta.progress(
            workplace=directory,
            git_url="git@gitee.com:floozy/springdemo.git",
            git_ref="refs/heads/master"
        )


class TestProd(unittest.TestCase):

    def test_tag(self):
        ci_docker_prod.progress(
            workplace=directory,
            git_url="git@gitee.com:floozy/springdemo.git",
            git_ref="refs/tags/v2.0.42"
        )


if __name__ == "__main__":
    unittest.main()
