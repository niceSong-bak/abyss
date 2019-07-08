# -*- coding: utf-8 -*-
# @Time : 2019-06-26 15:16
# @Email : aaronlzxian@163.com
# @File : config.py

from .config_parser import CI_BUILD_COMMAND_RELEASE, CI_BUILD_COMMAND_BETA

class Base():
    DOCKER_REGISTRY = "registry.cn-zhangjiakou.aliyuncs.com/floozy"

class Beta:
    class Land(Base):
        DOCKER_REGISTRY = "registry.cn-zhangjiakou.aliyuncs.com/plantation"
        DOCKER_ACCOUNT = "季诺科技"
        DOCKER_PASSWORD = "H32Npgzl"

class Prod:
    class Land(Base):
        DOCKER_REGISTRY = "registry.cn-zhangjiakou.aliyuncs.com/floozy"
        DOCKER_ACCOUNT = "季诺科技"
        DOCKER_PASSWORD = "H32Npgzl"

    class Ocean(Base):
        NAME = "ocean"
        DOCKER_REGISTRY = "837040555638.dkr.ecr.ap-southeast-1.amazonaws.com"

    class Twisted(Base):
        NAME = "twisted"
        DOCKER_REGISTRY = "402852579574.dkr.ecr.ap-southeast-1.amazonaws.com"

config = {
    CI_BUILD_COMMAND_BETA : Beta.Land,

    CI_BUILD_COMMAND_RELEASE: {
        "land": Prod.Land,
        "ocean": Prod.Ocean,
        "twisted": Prod.Twisted,
    },

    "default": Beta.Land
}

if __name__ == "__main__":
    config["release"]["ocean"]


