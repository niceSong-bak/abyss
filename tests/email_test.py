#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import unittest

from abyss import email_notifier

directory = '../build'
if not os.path.exists(directory):
    os.makedirs(directory)


class TestTag(unittest.TestCase):

    def test_email(self):
        email_notifier.send_email(
                to=['zhuchenxi@jinuo.me'],
                pipe='docker_prod',
                project_name='twisted-manager-backend',
                project_version='v1.2.4',
                message='互联网公司反腐继续劲吹',
                result=True
        )


if __name__ == "__main__":
    unittest.main()
