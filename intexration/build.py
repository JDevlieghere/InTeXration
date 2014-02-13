import os
import shutil
import tempfile


class Identifier:

    SEPARATOR = '/'

    def __init__(self, owner, repository, name):
        self.owner = owner
        self.repository = repository
        self.name = name

    def __str__(self):
        return self.owner + self.SEPARATOR + self.repository + self.SEPARATOR + self.name

    def __hash__(self):
        return hash((self.owner, self.repository, self.name))

    def __eq__(self, other):
        return (self.owner, self.repository, self.name) == (other.owner, other.repository, other.name)


class BuildRequest:

    def __init__(self, owner, repository, commit):
        self.owner = owner
        self.repository = repository
        self.commit = commit
        self._temp = tempfile.mkdtemp()

    def ssh_url(self):
        return 'git@github.com:'+self.owner+'/'+self.repository+'.git'

    def https_url(self):
        return 'https://github.com/'+self.owner+'/'+self.repository+'.git'

class Build:

    def __init__(self, path, tex, idx, bib):
        self.path = path
        self.tex = tex
        self.idx = idx
        self.bib = bib
        self._finished = False
        if not self.exist():
            raise RuntimeError("The necessary build files do not exist")

    def __set__(self, instance, path):
        self._check_finished()
        if not os.path.exists(path):
            raise RuntimeError('The given build path does not exist')
        else:
            self.path = path

    def __str__(self):
        return '[' + self.tex + ', ' + self.idx + ', ' + self.bib + ']'

    def exist(self):
        self._check_finished()
        return self.exist_tex()

    def path_idx(self):
        self._check_finished()
        return os.path.join(self.path, self.idx)

    def path_bib(self):
        self._check_finished()
        return os.path.join(self.path, self.bib)

    def path_tex(self):
        self._check_finished()
        return os.path.join(self.path, self.tex)

    def exist_idx(self):
        self._check_finished()
        return os.path.exists(self.path_idx())

    def exist_bib(self):
        self._check_finished()
        return os.path.exists(self.path_bib())

    def exist_tex(self):
        self._check_finished()
        return os.path.exists(self.path_tex())

    def _check_finished(self):
        if self.is_finished():
            raise RuntimeError("Cannot operate on finished build")
        return

    def is_finished(self):
        return self._finished

    def finish(self):
        self._check_finished()
        shutil.rmtree(self.path)
        self._finished = True

    def move_to(self, path):
        self._check_finished()
        # Current Paths
        old_idx = self.path_idx()
        old_bib = self.path_bib()
        old_tex = self.path_tex()
        # New Paths
        self.path = path
        new_idx = self.path_idx()
        new_bib = self.path_bib()
        new_tex = self.path_tex()
        # Move All
        if self.exist_idx():
            shutil.move(old_idx, new_idx)
        if self.exist_bib():
            shutil.move(old_bib, new_bib)
        shutil.move(old_tex, new_tex)