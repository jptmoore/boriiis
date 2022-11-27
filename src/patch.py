from git import Repo

class Patch:
    def __init__(self, ctx):
        self.local_repo = Repo(ctx.local_repo)

    def diff(self, ctx):
        content = self.local_repo.git.diff("origin/master", "master")
        return content