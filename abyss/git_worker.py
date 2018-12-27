#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import subprocess
import shutil
from abyss import logger as LOG

__author__ = "Jude"


class GitWorker:
    def __init__(self, workplace, url, ref):
        self.GIT_URL = url
        self.WORKPLACE = workplace
        self.REF = ref
        self.PROJECT_PATH = "unknown"

        """parse refs"""
        refs_paths = ref.split('/')
        if refs_paths[0] != 'refs':
            LOG.error("refs is invalid: " + ref)

        if refs_paths[1] == 'tags':
            self.TAG = refs_paths[2]
        elif refs_paths[1] == 'heads':
            self.TAG = refs_paths[2]
        else:
            LOG.error("unsupported ref: " + ref)

    def pull_code(self):
        """
        从gitSource 拉取code
        :return:
        true: 代码拉取成功
        false: 代码拉取失败
        """
        LOG.big_log_start("Start Pull Code")

        # clean
        LOG.debug('Start clean workplace: ' + self.WORKPLACE)
        shutil.rmtree(self.WORKPLACE)
        os.mkdir(self.WORKPLACE)
        LOG.debug('Start Downloading Source Code')

        # clone
        LOG.debug('git clone {repo}'.format(repo=self.GIT_URL))

        clone = subprocess.call('git clone {repo}'.format(repo=self.GIT_URL), shell=True, cwd=self.WORKPLACE)
        if clone != 0:
            LOG.error("git clone failed")
            return False

        # find project
        self.PROJECT_PATH = os.path.join(self.WORKPLACE,
                                         subprocess.check_output('ls -d [!_]*', shell=True, cwd=self.WORKPLACE).decode(
                                             'utf-8').split('\n')[0])
        LOG.debug("Project path: " + self.PROJECT_PATH)

        refs_paths = self.REF.split('/')
        coPoint = refs_paths[2]

        # checkout
        LOG.debug('git checkout {coPoint}'.format(coPoint=coPoint))
        checkout = subprocess.call('git checkout {coPoint}'.format(coPoint=coPoint), shell=True, cwd=self.PROJECT_PATH)
        if checkout != 0:
            LOG.error("git checkout failed")
            return False
        LOG.big_log_end("Pull Success")
        return True

    def copy_project(self, target):
        """
        复制到指定目录
        :param target: 指定目录
        :return:
        true: 复制成功
        false: 复制失败
        """
        LOG.big_log_start("Start copy project")

        # clean
        shutil.rmtree(target)
        os.mkdir(target)
        # copy
        cp = subprocess.call(LOG.debug(
            'cp -a * ' + target),
            shell=True, cwd=self.PROJECT_PATH)
        if cp != 0:
            LOG.error("code copy failed")
            return False
        LOG.big_log_end("Copy Success")
        return True

    def get_commit(self):
        """
        读当前的commit信息
        :return: (commit hash, timestamp, format time, commit message)
        """
        commit = subprocess.check_output('git show --format="%h|#|%ct|#|%ci|#|%s" --quiet'.format(tag=self.TAG),
                                         shell=True,
                                         cwd=self.PROJECT_PATH).decode('utf-8')
        commit_info = commit.split('|#|')
        # (commit hash, timestamp, format time, commit message)
        return commit_info[0], commit_info[1], commit_info[2], commit_info[3]
