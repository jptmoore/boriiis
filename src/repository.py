from git import Repo

class Repository:
    def __init__(self, ctx):
        self.local_repo = ctx.local_repo
        self.remote_repo = ctx.remote_repo

    def clone(self):
        try:
            repo = Repo.clone_from(self.remote_repo, self.local_repo)
            assert repo.__class__ is Repo
            return repo
        except Exception as e:
            print(e)
            return None