#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Jude"

import logging
import hashlib
import os
import subprocess
import sys
import yaml
import ci_notify

LOG = logging.getLogger('BuildLogger')
LOG.setLevel(logging.DEBUG)
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(levelname)s] %(asctime)s %(message)s')
console.setFormatter(formatter)
LOG.addHandler(console)

DOCKER_REGISTRY = "registry.cn-zhangjiakou.aliyuncs.com/floozy"
CI_CONFIG_FILE = "abyss.yaml"
CI_BUILD_COMMAND = "build"
CI_DEPLOY_REPO_NAME = "name"
CI_NOTIFY_EMAIL = "email"


class Utils:
    @classmethod
    def md5(cls, file_path):
        with open(file_path, 'rb') as f:
            md5obj = hashlib.md5()
            md5obj.update(f.read())
            return md5obj.hexdigest()

    @classmethod
    def md5str(cls, ori_str):
        m = hashlib.md5()
        m.update(ori_str)
        return m.hexdigest()

    @classmethod
    def size(cls, file_path):
        try:
            thesize = os.path.getsize(file_path)
            return str(thesize)
        except Exception as err:
            return str(0)


class Builder:
    def __init__(self, params_dic):
        # 传参
        self.build_params_dic = params_dic

        self.GIT_URL = params_dic.get('git_url')
        self.GIT_REF = params_dic.get('git_ref')
        self.PROJECT_PATH = params_dic.get('project_path')
        self.TAG = self.GIT_REF.split('/')[-1]

        self.WORKSPACE_BASE = params_dic.get('WORKSPACE')
        self.WORKSPACE_DOWNLOAD = self.WORKSPACE_BASE + '/download/'
        self.WORKSPACE_BUILD = self.WORKSPACE_BASE + '/build/'
        self.WORKSPACE_PACKAGE = self.WORKSPACE_BASE + '/package/'

        self.CONFIG = None

    def big_log(self, msg):
        LOG.debug('\n')
        LOG.debug('********************************************************************************')
        LOG.debug(msg)
        LOG.debug('********************************************************************************')

    def prepare_workspace(self):
        """
        准备 Jenkins 下的工作空间
        :return: 空
        """
        self.big_log('Preparing Jenkins Workspace')
        workspace_dirs = [self.WORKSPACE_DOWNLOAD, self.WORKSPACE_BUILD, self.WORKSPACE_PACKAGE]
        for the_dir in workspace_dirs:
            if os.path.exists(the_dir):
                LOG.debug('rm -R -f ' + the_dir + '*')
                clear = subprocess.call('rm -R -f ' + the_dir + '*', shell=True)
                if clear != 0:
                    logging.error("clear " + the_dir + " failed")
                    return False
            else:
                os.makedirs(the_dir)
        self.big_log('Preparing Workspace Done')
        return True

    def pull_code(self):
        """
        从gitSource 拉取code
        :return:
        0: 代码拉取成功
        -1: 代码拉取失败
        """
        self.big_log('Start Downloading Source Code')

        # clone
        LOG.debug('git clone {repo}'.format(repo=self.GIT_URL))
        clone = subprocess.call('git clone {repo}'.format(repo=self.GIT_URL), shell=True, cwd=self.WORKSPACE_DOWNLOAD)
        if clone != 0:
            logging.error("git clone failed")
            return False

        # checkout
        LOG.debug('git checkout {tag}'.format(tag=self.TAG))
        checkout = subprocess.call('git checkout {tag}'.format(tag=self.TAG), shell=True,
                                   cwd=self.WORKSPACE_DOWNLOAD + self.PROJECT_PATH)
        if checkout != 0:
            logging.error("git checkout failed")
            return False

        # copy
        cp = subprocess.call(
            'cp -a ' + self.WORKSPACE_DOWNLOAD + '/' + self.PROJECT_PATH + '/* ' + self.WORKSPACE_BUILD,
            shell=True)
        if cp != 0:
            logging.error("code copy failed")
            return False

        return True

    def build(self):
        """
        编译阶段
        :return: True or False 编译是否成功
        """
        f = open(self.WORKSPACE_BUILD + CI_CONFIG_FILE)
        self.CONFIG = yaml.load(f)

        for command in self.CONFIG[CI_BUILD_COMMAND]:
            LOG.debug(command)
            build_project = subprocess.call(command, shell=True,
                                            cwd=self.WORKSPACE_BUILD)
            if build_project != 0:
                logging.error("Project build failed")
                return False

        return True

    def push_docker(self):
        """
        上传镜像阶段
        :return: True or False PUSH是否成功
        """
        self.big_log('Start Login Docker Registry')

        tag_latest = subprocess.call(
            'docker login -u 季诺科技 -p aaron123 {registry}'.format(
                registry=DOCKER_REGISTRY), shell=True, cwd=self.WORKSPACE_BUILD)
        if tag_latest != 0:
            logging.error("Docker Tag latest failed")
            return False

        self.big_log('Start TAG Docker Image')
        LOG.debug("repo " + self.CONFIG.get(CI_DEPLOY_REPO_NAME))
        imageID = subprocess.check_output('docker images -q {repo}'.format(repo=self.CONFIG.get(CI_DEPLOY_REPO_NAME)),
                                          shell=True).decode('utf-8').split('\n')[0]
        if imageID == "":
            logging.error("Image not fond: " + self.CONFIG.get(CI_DEPLOY_REPO_NAME))
            return False

        tag_latest = subprocess.call(
            'docker tag {imageID} {registry}/{repo}:latest'.format(
                imageID=imageID, registry=DOCKER_REGISTRY, repo=self.CONFIG.get(CI_DEPLOY_REPO_NAME)), shell=True)
        if tag_latest != 0:
            logging.error("Docker Tag latest failed")
            return False

        tag_version = subprocess.call(
            'docker tag {imageID} {registry}/{repo}:{tag}'.format(
                imageID=imageID, registry=DOCKER_REGISTRY, repo=self.CONFIG.get(CI_DEPLOY_REPO_NAME), tag=self.TAG),
            shell=True)
        if tag_version != 0:
            logging.error("Docker Tag " + self.TAG + " failed")
            return False

        self.big_log('Start Push Docker Image')

        push_latest = subprocess.call(
            'docker push {registry}/{repo}:latest'.format(
                registry=DOCKER_REGISTRY, repo=self.CONFIG.get(CI_DEPLOY_REPO_NAME)), shell=True)
        if push_latest != 0:
            logging.error("Docker push " + self.TAG + " failed")
            return False

        push_version = subprocess.call(
            'docker push {registry}/{repo}:{tag}'.format(
                registry=DOCKER_REGISTRY, repo=self.CONFIG.get(CI_DEPLOY_REPO_NAME), tag=self.TAG), shell=True)
        if push_version != 0:
            logging.error("Docker push " + self.TAG + " failed")
            return False

        return True

    def send_email(self):
        self.big_log('Start Send Email')
        if ci_notify.send_email(self.CONFIG.get(CI_NOTIFY_EMAIL), self.CONFIG.get(CI_DEPLOY_REPO_NAME), self.TAG):
            logging.info("Send Email Success")
        else:
            logging.error("Send Email failed")
        return True


if __name__ == "__main__":
    build_param_dic = {}
    error_exit = False

    build_param_dic['WORKSPACE'] = os.environ['WORKSPACE']
    build_param_dic['git_url'] = os.environ['git_ssh_url']
    build_param_dic['git_ref'] = os.environ['ref']
    build_param_dic['project_path'] = os.environ['project_path']

    builder = Builder(build_param_dic)

    try:
        if builder.prepare_workspace() \
                and builder.pull_code() \
                and builder.build() \
                and builder.push_docker() \
                and builder.send_email():

            builder.big_log("Build Success")
        else:
            error_exit = True
    except Exception as e:
        LOG.error("Exception is " + str(e))
        error_exit = True
    finally:
        if error_exit:
            builder.big_log("Jenkins Job Failed!")
            sys.exit(-1)
        else:
            builder.big_log("Jenkins Job DONE!")
