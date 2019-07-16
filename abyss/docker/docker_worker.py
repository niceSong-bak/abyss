#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import subprocess
import shutil
from abyss import logger as LOG

__author__ = "Jude"


class DockerWorker:
    def __init__(self, registry,  image, module_name):
        self.REGISTRY = registry
        self.IMAGE = image
        self.module_name = module_name

    def login(self,account, password):
        LOG.big_log_start('Start Login Docker Registry')
        result = subprocess.call(LOG.debug(
            'docker login -u {account} -p {password} {registry}'.format(
                account=account,
                password=password,
                registry=self.REGISTRY)), shell=True)
        if result != 0:
            LOG.error("login failed")
            return False
        LOG.big_log_end('Login Success')
        return True

    def login_aws(self, name):
        result = subprocess.call(LOG.debug(
            "$(aws ecr get-login --no-include-email --region ap-southeast-1 --profile {name})".format(name=name)), shell=True)
        if result != 0:
            LOG.error("login failed")
            return False
        return True

    def tag(self, repo, tag):
        LOG.big_log_start('[{m}] Start TAG Docker Image'.format(m=self.module_name))

        imageID = \
            subprocess.check_output(LOG.debug('docker images -q {image}'.format(image=self.IMAGE)),
                                    shell=True).decode('utf-8').split('\n')[0]
        if imageID == "":
            LOG.error("[{m}] Image not fond: ".format(m=self.module_name) + self.IMAGE)
            return False

        result = subprocess.call(LOG.debug(
            'docker tag {imageID} {repo}:{tag}'.format(
                imageID=imageID, repo=repo, tag=tag)), shell=True)
        if result != 0:
            LOG.error("Docker Tag failed for: ")
            return False
        LOG.big_log_end('Tag Success')
        return True

    def push(self, repo, tag):
        """
        上传镜像阶段
        :return: True or False PUSH是否成功
        """
        LOG.big_log_start('[{m}] Start Push Docker Image'.format(m=self.module_name))

        push_latest = subprocess.call(LOG.debug(
            'docker push {repo}:{tag}'.format(
                repo=repo, tag=tag)), shell=True)
        if push_latest != 0:
            LOG.error("[{m}] Docker push  failed".format(m=self.module_name))
            return False
        LOG.big_log_end('[{m}] Push Success'.format(m=self.module_name))
        return True
