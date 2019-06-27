# -*- coding: utf-8 -*-
# @Time : 2019-06-26 16:51
# @Email : aaronlzxian@163.com
# @File : ci_docker.py
import os
import subprocess

from abyss.config_parser import ConfigParser
from abyss.docker.docker_worker import DockerWorker
from abyss.file_manager import FileManager
from abyss.git_worker import GitWorker
from abyss import logger as LOG, email_notifier
from abyss.config import config

class CIDocker():
    def __init__(self, pipe, workplace, git_url, git_ref):
        self.pipe = pipe
        self.workplace = workplace
        self.git_url = git_url
        self.git_ref = git_ref

    def pre_workplace(self):
        self.file_manager = FileManager(self.workplace)
        self.file_manager.prepare()

    def git_process(self):
        # Git下载  ============================================================================================
        self.git_worker = GitWorker(self.file_manager.WORKSPACE_DOWNLOAD, self.git_url, self.git_ref)
        if not self.git_worker.pull_code():
            raise Exception("pull code failed")
        if not self.git_worker.copy_project(self.file_manager.WORKSPACE_BUILD):
            raise Exception("copy project failed")

    def pre_env(self):
        # 准备环境  ============================================================================================
        LOG.big_log_start("Start Build")

        new_env = {}
        new_env['pipe'] = self.pipe
        commit = self.git_worker.get_commit()
        new_env['version'] = self.git_worker.BRANCH.replace("/", "-") + "-" + commit[0]
        new_env['commitId'] = commit[0]
        new_env['commitTime'] = commit[1]
        new_env['commitTimeFormat'] = commit[2]
        new_env['commitMessage'] = commit[3]

        for k in new_env:
            LOG.debug("new_env[{key}] = {value}".format(key=k, value=new_env[k]))

        new_env.update(os.environ.copy())

        self.new_env = new_env

    def docker_process(self):
        self.abyss_config = ConfigParser(self.file_manager.WORKSPACE_BUILD, self.pipe)
        # 真正的build  ================================================================================================
        for command in self.abyss_config.build():
            build_project = subprocess.call(LOG.debug(command), shell=True,
                                            cwd=self.file_manager.WORKSPACE_BUILD, env=self.new_env)
            if build_project != 0:
                raise Exception("Project build failed")

        LOG.big_log_end("Build Success")
        self.release = self.abyss_config.deploy_release()
        if isinstance(config[self.pipe], dict):
            registry_config = config[self.pipe][self.release]
        else:
            registry_config = config[self.pipe]
        LOG.debug("Deploy release: {release}".format(release=self.release))

        # 处理镜像  ================================================================================================
        docker_worker = DockerWorker(
            registry=registry_config.DOCKER_REGISTRY,
            image=self.abyss_config.image()
        )

        self.login_docker_repository(docker_worker, registry_config)

        repo_name = registry_config.DOCKER_REGISTRY + "/" + self.abyss_config.repo()

        if not docker_worker.tag(repo_name, self.git_worker.TAG):
            raise Exception("tag failed")

        if not docker_worker.push(repo_name, self.git_worker.TAG):
            raise Exception("push failed")

        if not docker_worker.tag(repo_name, 'latest'):
            raise Exception("tag latest failed")

        if not docker_worker.push(repo_name, 'latest'):
            raise Exception("push latest failed")

    def login_docker_repository(self, docker_worker, registry_config):
        if hasattr(registry_config, 'DOCKER_ACCOUNT') and hasattr(registry_config, 'DOCKER_PASSWORD'):
            docker_worker.login(registry_config.DOCKER_ACCOUNT, registry_config.DOCKER_PASSWORD)
        elif hasattr(registry_config, 'NAME'):
            docker_worker.login_aws(registry_config.NAME)
        else:
            raise Exception("Login docker repository failed")

    def notify(self):
        # 通知  ================================================================================================
        if not email_notifier. send_email(
                to=self.abyss_config.email(),
                pipe=self.pipe,
                project_name=self.self.abyss_config.image(),
                project_version=self.git_worker.BRANCH,
                message=self.git_worker.get_commit()[3],
                result=True,
                release=self.release
        ):
            raise Exception("send email failed")
        return True

    def ci_process(self):
        result = True
        try:
            self.pre_workplace()
            self.git_process()
            self.pre_env()
            self.docker_process()
        except:
            result = False
        finally:
            self.notify()
            return result
