#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
from abyss.docker import ci_docker_beta, ci_docker_prod, ci_docker_aws, ci_docker_ocean
from abyss import logger as LOG

__author__ = "Jude"

PIPES = {
    "docker_beta": ci_docker_beta,
    "docker_prod": ci_docker_prod,
    "docker_aws": ci_docker_aws,
    "docker_ocean": ci_docker_ocean,
}

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

    if pipe not in PIPES:
        LOG.error("unknown pipe: " + pipe)
        sys.exit(1)

    if not PIPES[pipe].progress(pipe, workplace, git_url, git_ref):
        LOG.big_log_start("Jenkins Job Failed!")
        sys.exit(1)

    LOG.big_log_start("Jenkins Job Success!")


