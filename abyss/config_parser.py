#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import yaml

from abyss import logger as LOG

__author__ = "Jude"

CI_BUILD_COMMAND = "build"
CI_BUILD_COMMAND_RELEASE = "prod"
CI_BUILD_COMMAND_BETA = "beta"
CI_DEPLOY_IMAGE_NAME = "name"
CI_DEPLOY_REPO_NAME = "repo"
CI_NOTIFY_EMAIL = "email"
CI_DEPLOY_RELEASE = "release"


class ConfigParser:
    def __init__(self, project_path, pipe):
        config_path = os.path.join(project_path, "abyss.yaml")
        LOG.debug("find abyss.yaml in "+config_path)
        if not os.path.exists(config_path):
            config_path = os.path.join(project_path, "abyss.yml")
            LOG.debug("find abyss.yml in " + config_path)
            if not os.path.exists(config_path):
                LOG.error("abyss.yaml nofound")

        with open(config_path, 'r') as f:
            for line in f.readlines():
                LOG.debug(line.strip())

        f = open(config_path, 'r')
        self.CONFIG = yaml.load(f)
        f.close()
        self.pipe = pipe

    def image(self):
        return self.CONFIG.get(CI_DEPLOY_IMAGE_NAME)

    def repo(self):
        if CI_DEPLOY_REPO_NAME in self.CONFIG:
            return self.CONFIG.get(CI_DEPLOY_REPO_NAME)
        else:
            return self.CONFIG.get(CI_DEPLOY_IMAGE_NAME)

    def build_release(self):
        return self.CONFIG.get(CI_BUILD_COMMAND)[CI_BUILD_COMMAND_RELEASE]

    def build_beta(self):
        return self.CONFIG.get(CI_BUILD_COMMAND)[CI_BUILD_COMMAND_BETA]

    def build(self):
        return self.CONFIG.get(CI_BUILD_COMMAND)[self.pipe]

    def email(self):
        return self.CONFIG.get(CI_NOTIFY_EMAIL)

    def deploy_release(self):
        return self.CONFIG.get(CI_DEPLOY_RELEASE)


