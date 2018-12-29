#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import subprocess
import sys

from abyss.config_parser import ConfigParser
from abyss.docker.docker_worker import DockerWorker
from abyss.file_manager import FileManager
from abyss.git_worker import GitWorker
from abyss import logger as LOG, email_notifier

__author__ = "Jude"

AWS_DOCKER_REGISTRY = "402852579574.dkr.ecr.ap-southeast-1.amazonaws.com"
"""
新jenkins slaver机器需要安装配置 aws cli
"""


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

        version = re.sub('^v(?=\d+)', '', git_worker.TAG)
        new_env['version'] = version

        commit = git_worker.get_commit()
        new_env['commitId'] = commit[0]
        new_env['commitTime'] = commit[1]
        new_env['commitTimeFormat'] = commit[2]
        new_env['commitMessage'] = commit[3]

        # 真正的build  ============================================================================================
        for command in abyss_config.build_beta():
            build_project = subprocess.call(LOG.debug(command), shell=True,
                                            cwd=file_manager.WORKSPACE_BUILD, env=new_env)
            if build_project != 0:
                raise Exception("Project build failed")

        # 处理镜像  ============================================================================================
        docker_worker = DockerWorker(
            registry=AWS_DOCKER_REGISTRY,
            image=abyss_config.image()
        )

        if not docker_worker.login_aws():
            raise Exception("registry login failed")

        repo_name = AWS_DOCKER_REGISTRY + "/" + abyss_config.repo()

        if not docker_worker.tag(repo_name, git_worker.TAG):
            raise Exception("tag failed")

        if not docker_worker.push(repo_name, git_worker.TAG):
            raise Exception("push failed")

        # 通知  ============================================================================================
        if not email_notifier.send_email(
                to=abyss_config.email(),
                project_name=abyss_config.image(),
                project_version=git_worker.TAG,
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
                    project_version=git_worker.TAG,
                    message="Error: " + str(e),
                    result=False
            ):
                LOG.big_log_start("Error email send failed")
        return False
