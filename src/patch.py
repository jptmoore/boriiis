from git import Repo
from pp import pp_exit

class Patch:
    def __init__(self, ctx):
        self.local_repo = ctx.local_repo
        self.log = ctx.log

    def diff(self):
        try:
            repo = Repo(self.local_repo)
            assert repo.__class__ is Repo
            content = repo.git.diff("origin/master", "master")
            return content
        except Exception as e:
            pp_exit("failed to create diff")
