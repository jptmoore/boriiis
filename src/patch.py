from git import Repo

class Patch:
    def __init__(self, ctx):
        self.repo = Repo("/home/john/git/miiify/db")

    def diff(self, ctx):
        content = self.repo.git.diff("origin/master", "master")
        return content