from git import Repo
import shutil
import os

from pp import pp_exit

class Repository:
    def __init__(self, ctx):
        self.local_repo = ctx.local_repo
        self.remote_repo = ctx.remote_repo
        self.log = ctx.log

    def __remove__(self):
        if os.path.exists(self.local_repo):
            try:
                shutil.rmtree(self.local_repo)
            except Exception as e:
                pp_exit("failed to remove existing repository")
            else:
                pass

    def clone(self):
        self.__remove__()
        try:
            repo = Repo.clone_from(self.remote_repo, self.local_repo)
            assert repo.__class__ is Repo
            return repo
        except Exception as e:
            pp_exit("failed to clone repository")
