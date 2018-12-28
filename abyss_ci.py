#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
from abyss.docker import ci_docker_beta, ci_docker_prod, ci_docker_aws

__author__ = "Jude"

PIPES = {
    "docker_beta": ci_docker_beta,
    "docker_prod": ci_docker_prod,
    "docker_aws": ci_docker_aws
}

if __name__ == "__main__":

    if "pipe" in os.environ:
        pipe = os.environ['pipe']
    else:
        raise Exception("Missing pipe")

    if "WORKSPACE" in os.environ:
        workplace = os.environ['WORKSPACE']
    else:
        raise Exception("Missing workplace")

    if "git_ssh_url" in os.environ:
        git_url = os.environ['git_ssh_url']
    else:
        raise Exception("Missing git_ssh_url")

    if "ref" in os.environ:
        git_ref = os.environ['ref']
    else:
        raise Exception("Missing git_ref")

    if pipe in PIPES:
        PIPES[pipe].build(workplace, git_url, git_ref)
    else:
        raise Exception("unknown pipe: " + pipe)

