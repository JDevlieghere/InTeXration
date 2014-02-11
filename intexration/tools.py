import contextlib
import os
import errno


@contextlib.contextmanager
def cd(directory):
    cur_dir = os.getcwd()
    try:
        os.chdir(directory)
        yield
    finally:
        os.chdir(cur_dir)


def create_dir(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise
    return path