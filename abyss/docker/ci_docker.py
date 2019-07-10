# -*- coding: utf-8 -*-
# @Time : 2019-06-26 16:51
# @Email : aaronlzxian@163.com
# @File : ci_docker.py
import os
import subprocess
import traceback

from abyss.config_parser import ConfigParser
from abyss.docker.docker_worker import DockerWorker
from abyss.file_manager import FileManager
from abyss.git_worker import GitWorker
from abyss.module_parser import ModuleParser
from abyss.modify_commit import ModifyCommit
from abyss import logger as LOG, email_notifier
from abyss.config import config

class CIDocker():
    def __init__(self, pipe, workplace, git_url, git_ref, commits):
        self.pipe = pipe
        self.workplace = workplace
        self.git_url = git_url
        self.git_ref = git_ref
        self.transfer_commits(commits)

    def transfer_commits(self, commits):
        self.commits = ModifyCommit.process_multiple_commits(commits)

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

    def build_modules(self):
        module_parser = ModuleParser(self.file_manager.WORKSPACE_BUILD)
        modules = module_parser.modify_modules(self.commits)
        self.short_module_names = module_parser.short_module_names
        for module in modules:
            self.docker_process(module)

    def docker_process(self, module):
        if module == self.file_manager.WORKSPACE_BUILD:
            self.short_module_name = 'All'
        else:
            self.short_module_name = module.replace(self.file_manager.WORKSPACE_BUILD+'/', '')

        LOG.big_log_start("[{m}] Start Build".format(m=self.short_module_name))
        self.abyss_config = ConfigParser(module, self.pipe)
        # 真正的build  ================================================================================================
        for command in self.abyss_config.build():
            build_project = subprocess.call(LOG.debug(command), shell=True,
                                            cwd=self.file_manager.WORKSPACE_BUILD, env=self.new_env)
            if build_project != 0:
                raise Exception("[{m}] Module build failed".format(m=self.short_module_name))

        LOG.big_log_end("[{m}] Build Module Success".format(m=self.short_module_name))
        self.release = self.abyss_config.deploy_release()
        if isinstance(config[self.pipe], dict):
            registry_config = config[self.pipe][self.release]
        else:
            registry_config = config[self.pipe]
        LOG.debug("[{m}] Deploy release: {release}".format(m=self.short_module_name, release=self.release))

        # 处理镜像  ================================================================================================
        docker_worker = DockerWorker(
            registry=registry_config.DOCKER_REGISTRY,
            image=self.abyss_config.image(),
            module_name=self.short_module_name
        )

        self.login_docker_repository(docker_worker, registry_config)

        repo_name = registry_config.DOCKER_REGISTRY + "/" + self.abyss_config.repo()

        if not docker_worker.tag(repo_name, self.git_worker.TAG):
            raise Exception("[{m}] tag failed".format(m=self.short_module_name))

        if not docker_worker.push(repo_name, self.git_worker.TAG):
            raise Exception("[{m}] push failed".format(m=self.short_module_name))

        if not docker_worker.tag(repo_name, 'latest'):
            raise Exception("[{m}] tag latest failed".format(m=self.short_module_name))

        if not docker_worker.push(repo_name, 'latest'):
            raise Exception("[{m}] push latest failed".format(m=self.short_module_name))

    def login_docker_repository(self, docker_worker, registry_config):
        if hasattr(registry_config, 'DOCKER_ACCOUNT') and hasattr(registry_config, 'DOCKER_PASSWORD'):
            docker_worker.login(registry_config.DOCKER_ACCOUNT, registry_config.DOCKER_PASSWORD)
        elif hasattr(registry_config, 'NAME'):
            docker_worker.login_aws(registry_config.NAME)
        else:
            raise Exception("Login docker repository failed")

    def notify(self, result=True):
        # 通知  ================================================================================================
        if not hasattr(self, 'release'):
            self.release = "未知"
        if not email_notifier.send_email(
                to=self.abyss_config.email(),
                module='|'.join(self.short_module_names),
                pipe=self.pipe,
                project_name=self.abyss_config.image(),
                project_version=self.git_worker.BRANCH,
                message=self.git_worker.get_commit()[3],
                result=result,
                release=self.release or ''
        ):
            raise Exception("send email failed")
        return True

    def ci_process(self):
        result = True
        try:
            self.pre_workplace()
            self.git_process()
            self.pre_env()
            self.build_modules()
        except Exception as e:
            LOG.big_log_end("Build Error")
            LOG.error(traceback.format_exc())
            result = False
        finally:
            self.notify(result)
            return result
