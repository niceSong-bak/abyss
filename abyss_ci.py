#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
from abyss.docker.ci_docker import CIDocker
from abyss import logger as LOG, config_parser

__author__ = "Jude"

def transfer(pipe):
    if pipe == "docker_prod" or pipe == "docker_aws" or pipe == "docker_ocean" or "release":
        return config_parser.CI_BUILD_COMMAND_RELEASE
    elif pipe == "docker_beta" or pipe == "beta" or pipe == "fucker":
        return config_parser.CI_BUILD_COMMAND_BETA
    else:
        LOG.error("unknown pipe: " + pipe)
        sys.exit(1)


if __name__ == "__main__":

    if "pipe" in os.environ:
        pipe = os.environ['pipe']
    else:
        LOG.error("Missing pipe")
        sys.exit(1)

    if "WORKSPACE" in os.environ:
        workplace = os.environ['WORKSPACE']
    else:
        LOG.error("Missing workplace")
        sys.exit(1)

    if "git_ssh_url" in os.environ:
        git_url = os.environ['git_ssh_url']
    else:
        LOG.error("Missing git_ssh_url")
        sys.exit(1)

    if "ref" in os.environ:
        git_ref = os.environ['ref']
    else:
        LOG.error("Missing git_ref")
        sys.exit(1)

    _pipe = transfer(pipe)

    if not CIDocker(
        workplace=workplace,
        git_url=git_url,
        git_ref=git_ref,
        pipe=_pipe
    ).ci_process():
        LOG.big_log_start("Jenkins Job Failed!")
        sys.exit(1)

    LOG.big_log_start("Jenkins Job Success!")


