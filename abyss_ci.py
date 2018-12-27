#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
from abyss.docker import ci_docker_beta, ci_docker_prod

__author__ = "Jude"

if __name__ == "__main__":
    pipe = sys.argv[1]

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

    if pipe == 'docker':
        ci_docker_prod.build(workplace, git_url, git_ref)
    elif pipe == 'docker_beta':
        ci_docker_beta.build(workplace, git_url, git_ref)
    else:
        raise Exception("unknown pipe: " + pipe)
