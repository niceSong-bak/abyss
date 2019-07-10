# -*- coding: utf-8 -*-
# @Time : 2019-06-28 15:22
# @Email : aaronlzxian@163.com
# @File : modify_commit.py
import json

class ModifyCommit:
    def __init__(self, commit):
        self.commit = commit
        self.author = commit['author']
        self.name = self.author['name']
        self.email = self.author['email']
        if 'remark' in self.author:
            self.remark = self.author['remark']
        self.modify_file()

    def modify_file(self):
        self.added = self.commit['added']
        self.removed = self.commit['removed']
        self.modified = self.commit['modified']
        self.modify_files = set(self.added).union(set(self.removed)).union(set(self.modified))

    @staticmethod
    def process_commit_info(commits):
        result = []
        for commit in commits:
            result.append(ModifyCommit(commit))
        return result

    @staticmethod
    def process_multiple_commits(commits):
        result = set()
        commits = commits.strip().replace('\n','')
        commits_json = json.loads(commits)
        commit_infos = ModifyCommit.process_commit_info(commits_json)
        for temp in commit_infos:
            result.update(temp.modify_files)
        return result



