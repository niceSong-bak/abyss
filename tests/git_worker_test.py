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
        self.git_worker = GitWorker(directory, "git@gitee.com:floozy/springdemo.git", "refs/tags/v2.1.16")

    def test_pull(self):
        self.git_worker.pull_code()

    def test_read_commit(self):
        self.git_worker.pull_code()
        print(self.git_worker.get_commit())

    def test_get_commit_recent_diff_file(self):
        self.git_worker.pull_code()
        print(self.git_worker.get_commit_recent_diff_file())


class TestPush(unittest.TestCase):
    def setUp(self):
        self.git_worker = GitWorker(directory, "git@gitee.com:floozy/springdemo.git", "refs/heads/devww")

    def test_pull(self):
        self.git_worker.pull_code()

    def test_read_commit(self):
        self.git_worker.pull_code()
        print(self.git_worker.get_commit())

    def test_get_commit_recent_diff_file(self):
        self.git_worker.pull_code()
        print(self.git_worker.get_commit_recent_diff_file())


if __name__ == "__main__":
    unittest.main()
