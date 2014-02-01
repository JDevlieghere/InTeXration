import contextlib
import logging
import os
import errno
import shutil


@contextlib.contextmanager
def cd(directory):
    cur_dir = os.getcwd()
    try:
        os.chdir(directory)
        yield
    finally:
        os.chdir(cur_dir)


def create_dir(path):
    """Safely create a directory."""
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    return path


# def empty(path, files_only=True):
#     if not os.path.exists(path):
#         return
#     for content in os.listdir(path):
#         content_path = os.path.join(path, content)
#         try:
#             os.remove(content_path)
#         except OSError:
#             if not files_only:
#                 shutil.rmtree(content_path)
#         except Exception as e:
#             logging.error(e)
#
#
# def remove(path):
#     if os.path.exists(path):
#         shutil.rmtree(path)