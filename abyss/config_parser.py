#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import subprocess
import shutil
import yaml

from abyss import logger as LOG

__author__ = "Jude"

CI_BUILD_COMMAND = "build"
CI_BUILD_COMMAND_RELEASE = "release"
CI_BUILD_COMMAND_BETA = "beta"
CI_DEPLOY_REPO_NAME = "name"
CI_NOTIFY_EMAIL = "email"


class ConfigParser:
    def __init__(self, project_path):
        config_path = os.path.join(project_path, "abyss.yaml")
        LOG.debug("find abyss.yaml in "+config_path)
        if not os.path.exists(config_path):
            config_path = os.path.join(project_path, "abyss.yml")
            LOG.debug("find abyss.yml in " + config_path)
            if not os.path.exists(config_path):
                LOG.error("abyss.yaml nofound")

        f = open(config_path)
        self.CONFIG = yaml.load(f)

    def image_name(self):
        return self.CONFIG.get(CI_DEPLOY_REPO_NAME)

    def build_release(self):
        return self.CONFIG.get(CI_BUILD_COMMAND)[CI_BUILD_COMMAND_RELEASE]

    def build_beta(self):
        return self.CONFIG.get(CI_BUILD_COMMAND)[CI_BUILD_COMMAND_BETA]

    def email(self):
        return self.CONFIG.get(CI_NOTIFY_EMAIL)
