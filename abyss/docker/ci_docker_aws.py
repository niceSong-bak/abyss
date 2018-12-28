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

__author__ = "Jude"

AWS_DOCKER_REGISTRY = "402852579574.dkr.ecr.ap-southeast-1.amazonaws.com"
"""
新jenkins slaver机器需要安装配置 aws cli
"""
def progress(workplace, git_url, git_ref):
    file_manager = FileManager(workplace)
    file_manager.prepare()
    # Git下载
    git_worker = GitWorker(file_manager.WORKSPACE_DOWNLOAD, git_url, git_ref)
    git_worker.pull_code()
    git_worker.copy_project(file_manager.WORKSPACE_BUILD)
    abyss_config = ConfigParser(file_manager.WORKSPACE_BUILD)

    new_env = os.environ.copy()
    new_env['pipe'] = os.environ['pipe']
    new_env['tag'] = git_worker.TAG
    commit = git_worker.get_commit()
    new_env['commitId'] = commit[0]
    new_env['commitTime'] = commit[1]
    new_env['commitTimeFormat'] = commit[2]
    new_env['commitMessage'] = commit[3]

    # 真正的build
    for command in abyss_config.build_beta():
        build_project = subprocess.call(LOG.debug(command), shell=True,
                                        cwd=file_manager.WORKSPACE_BUILD, env=new_env)
        if build_project != 0:
            LOG.error("Project build failed")
            return False
    # 处理镜像
    docker_worker = DockerWorker(
        registry=AWS_DOCKER_REGISTRY,
        image=abyss_config.image()
    )
    docker_worker.login_aws()
    repo_name = AWS_DOCKER_REGISTRY + "/" + abyss_config.repo()

    docker_worker.tag(repo_name, git_worker.TAG)
    docker_worker.push(repo_name, git_worker.TAG)

    # 通知
    email_notifier.send_email(
        to=abyss_config.email(),
        project_name=abyss_config.image(),
        project_version=git_worker.TAG,
        message=git_worker.get_commit()[3]
    )


def build(workplace, git_url, git_ref):
    error_exit = False
    try:
        progress(workplace, git_url, git_ref)
    except Exception as e:
        LOG.error("Exception is " + str(e))
        error_exit = True
    finally:
        if error_exit:
            LOG.big_log_start("Jenkins Job Failed!")
            sys.exit(-1)
        else:
            LOG.big_log_start("Jenkins Job DONE!")
