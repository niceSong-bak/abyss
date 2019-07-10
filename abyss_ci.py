#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import re
from abyss.docker.ci_docker import CIDocker
from abyss import logger as LOG, config_parser

__author__ = "Jude"

pattern = re.compile('^refs/((heads)/.+|(tags)/.+)$')
release = 'tags'
beta = 'heads'

def transfer(git_ref):

    p = pattern.findall(git_ref)
    if len(p) < 1:
        LOG.error("unknown git_ref: " + git_ref)
        sys.exit(1)

    if release in p[0]:
        return config_parser.CI_BUILD_COMMAND_RELEASE
    elif beta in p[0]:
        return config_parser.CI_BUILD_COMMAND_BETA
    else:
        LOG.error("unknown git_ref: " + git_ref)
        sys.exit(1)


if __name__ == "__main__":
    if "commits" in os.environ:
        commits = os.environ['commits']
    else:
        commits = None

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
    pipe = transfer(git_ref)

    LOG.debug(pipe)

    if not CIDocker(
        workplace=workplace,
        git_url=git_url,
        git_ref=git_ref,
        pipe=pipe,
        commits=commits
    ).ci_process():
        LOG.big_log_start("Jenkins Job Failed!")
        sys.exit(1)

    LOG.big_log_start("Jenkins Job Success!")


