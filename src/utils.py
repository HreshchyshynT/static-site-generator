from os import path as path
import os


def copy_files(src, dst):
    src = path.abspath(src)
    dst = path.abspath(dst)
    if not path.exists(src) or not path.isdir(src):
        raise Exception(f"{src} not exists or is not a directory")
    if not path.exists(dst):
        os.mkdir(dst)
    else:

        def remove(all, parent=""):
            for file in all:
                p = path.join(parent, file)
                if path.isdir(p):
                    remove(os.listdir(p), parent=p)
                else:
                    os.remove(p)

        remove([dst])
