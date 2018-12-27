#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import subprocess
import shutil
from abyss import logger as LOG

__author__ = "Jude"


class FileManager:
    def __init__(self, baseplace):
        self.WORKSPACE_BASE = baseplace
        self.WORKSPACE_DOWNLOAD = os.path.join(self.WORKSPACE_BASE, 'download')
        self.WORKSPACE_PACKAGE = os.path.join(self.WORKSPACE_BASE, 'package')
        self.WORKSPACE_BUILD = os.path.join(self.WORKSPACE_BASE, 'build')

    def prepare(self):
        LOG.big_log_start("prepare base workplace: " + self.WORKSPACE_BASE)
        shutil.rmtree(self.WORKSPACE_BASE)
        os.makedirs(self.WORKSPACE_BASE)
        os.makedirs(self.WORKSPACE_DOWNLOAD)
        os.makedirs(self.WORKSPACE_BUILD)
        os.makedirs(self.WORKSPACE_PACKAGE)

    def clean_download(self):
        LOG.big_log_start("clean_download")
        shutil.rmtree(self.WORKSPACE_DOWNLOAD)
        os.makedirs(self.WORKSPACE_DOWNLOAD)

    def clean_build(self):
        LOG.big_log_start("clean_build")
        shutil.rmtree(self.WORKSPACE_BUILD)
        os.makedirs(self.WORKSPACE_BUILD)

    def clean_package(self):
        LOG.big_log_start("clean_package")
        shutil.rmtree(self.WORKSPACE_PACKAGE)
        os.makedirs(self.WORKSPACE_PACKAGE)

