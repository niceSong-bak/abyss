#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import unittest

from abyss.docker.docker_worker import DockerWorker
from abyss.git_worker import GitWorker

ALIYUN_DOCKER_REGISTRY = "registry.cn-zhangjiakou.aliyuncs.com/plantation"
ALIYUN_DOCKER_ACCOUNT = "zhuchenxi@jinuo"
ALIYUN_DOCKER_PASSWORD = "uk5v4Xvb"

class TestDocker(unittest.TestCase):
    def setUp(self):
        self.docker_worker = DockerWorker(
            registry=ALIYUN_DOCKER_REGISTRY,
            account=ALIYUN_DOCKER_ACCOUNT,
            password=ALIYUN_DOCKER_PASSWORD,
            image="navigator"
        )

    def test_tag(self):
        self.docker_worker.login()
        self.docker_worker.tag(ALIYUN_DOCKER_REGISTRY, "test")
        self.docker_worker.push(ALIYUN_DOCKER_REGISTRY, "test")

if __name__ == "__main__":
    unittest.main()
