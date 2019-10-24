# -*- coding: utf-8 -*-
# @Time : 2019-06-26 15:16
# @Email : aaronlzxian@163.com
# @File : config.py

from .config_parser import CI_BUILD_COMMAND_BETA, CI_BUILD_COMMAND_RELEASE

class Base():
    DOCKER_REGISTRY = "082924159698.dkr.ecr.ap-northeast-1.amazonaws.com/orion"

class Beta:
    class Orion(Base):
        NAME = "orion"
        DOCKER_REGISTRY = "082924159698.dkr.ecr.ap-northeast-1.amazonaws.com"

config = {
    CI_BUILD_COMMAND_BETA: Beta.Land,

    "default": Beta.Land
}

if __name__ == "__main__":
    config["release"]["ocean"]


