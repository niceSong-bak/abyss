#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import subprocess
import sys

from abyss.config_parser import ConfigParser
from abyss.docker.docker_worker import DockerWorker
from abyss.file_manager import FileManager
from abyss.git_worker import GitWorker
from abyss import logger as LOG, email_notifier
import re

__author__ = "Jude"

ALIYUN_DOCKER_REGISTRY = "registry.cn-zhangjiakou.aliyuncs.com/floozy"
ALIYUN_DOCKER_ACCOUNT = "季诺科技"
ALIYUN_DOCKER_PASSWORD = "H32Npgzl"


def progress(pipe, workplace, git_url, git_ref):
    global file_manager
    global git_worker
    global abyss_config
    global docker_worker
    try:
        file_manager = FileManager(workplace)
        file_manager.prepare()

        # Git下载  ============================================================================================
        git_worker = GitWorker(file_manager.WORKSPACE_DOWNLOAD, git_url, git_ref)
        if not git_worker.pull_code():
            raise Exception("pull code failed")
        if not git_worker.copy_project(file_manager.WORKSPACE_BUILD):
            raise Exception("copy project failed")
        abyss_config = ConfigParser(file_manager.WORKSPACE_BUILD)

        # 准备环境  ============================================================================================
        new_env = os.environ.copy()
        new_env['pipe'] = pipe

        version = re.sub('^v(?=\d+)', '', git_worker.BRANCH)
        new_env['version'] = version

        commit = git_worker.get_commit()
        new_env['commitId'] = commit[0]
        new_env['commitTime'] = commit[1]
        new_env['commitTimeFormat'] = commit[2]
        new_env['commitMessage'] = commit[3]

        # 真正的build  ================================================================================================
        for command in abyss_config.build_release():
            build_project = subprocess.call(LOG.debug(command), shell=True,
                                            cwd=file_manager.WORKSPACE_BUILD, env=new_env)
            if build_project != 0:
                raise Exception("Project build failed")

        # 处理镜像  ================================================================================================
        docker_worker = DockerWorker(
            registry=ALIYUN_DOCKER_REGISTRY,
            image=abyss_config.image()
        )
        if not docker_worker.login(account=ALIYUN_DOCKER_ACCOUNT, password=ALIYUN_DOCKER_PASSWORD):
            raise Exception("registry login failed")

        repo_name = ALIYUN_DOCKER_REGISTRY + "/" + abyss_config.repo()

        if not docker_worker.tag(repo_name, git_worker.TAG):
            raise Exception("tag failed")

        if not docker_worker.push(repo_name, git_worker.TAG):
            raise Exception("push failed")

        if not docker_worker.tag(repo_name, 'latest'):
            raise Exception("tag latest failed")

        if not docker_worker.push(repo_name, 'latest'):
            raise Exception("push latest failed")

        # 通知  ================================================================================================
        if not email_notifier.send_email(
                to=abyss_config.email(),
                project_name=abyss_config.image(),
                project_version=git_worker.BRANCH,
                message=git_worker.get_commit()[3],
                result=True
        ):
            raise Exception("send email failed")

        return True
    except Exception as e:
        LOG.big_log_start("Error: " + str(e))
        # 失败  ================================================================================================
        if abyss_config is not None:
            if not email_notifier.send_email(
                    to=abyss_config.email(),
                    project_name=abyss_config.image(),
                    project_version=git_worker.BRANCH,
                    message="Error: " + str(e),
                    result=False
            ):
                LOG.big_log_start("Error email send failed")
        return False
