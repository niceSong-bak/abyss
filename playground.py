#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Jude

import subprocess

clone = subprocess.check_output('git tag -l v1.0.0 -n --format "%(subject)"', shell=True)
print(clone.decode('utf-8'))



