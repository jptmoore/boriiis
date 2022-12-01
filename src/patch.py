from git import Repo

class Patch:
    def __init__(self, ctx):
        self.local_repo = ctx.local_repo

    def diff(self):
        try:
            repo = Repo(self.local_repo)
            assert repo.__class__ is Repo
            content = repo.git.diff("origin/master", "master")
            return content
        except Exception as e:
            print(e)
            return None        