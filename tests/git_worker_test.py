#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import unittest

from abyss.git_worker import GitWorker

directory = '../build'
if not os.path.exists(directory):
    os.makedirs(directory)


class TestTag(unittest.TestCase):
    def setUp(self):
        self.git_worker = GitWorker(directory, "git@gitee.com:floozy/springdemo.git", "refs/tags/v2.0.42")

    def test_pull(self):
        self.git_worker.pull_code()

    def test_read_commit(self):
        self.git_worker.pull_code()
        print(self.git_worker.get_commit())


class TestPush(unittest.TestCase):
    def setUp(self):
        self.git_worker = GitWorker(directory, "git@gitee.com:floozy/springdemo.git", "refs/heads/master")

    def test_pull(self):
        self.git_worker.pull_code()

    def test_read_commit(self):
        self.git_worker.pull_code()
        print(self.git_worker.get_commit())


if __name__ == "__main__":
    unittest.main()
