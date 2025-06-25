from os import path as path
import os


def copy_files(src, dst):
    def do_recursive(what, all, parent=""):
        for file in all:
            p = path.join(parent, file)
            if path.isdir(p):
                do_recursive(what, os.listdir(p), parent=p)
            else:
                what(p)

    src = path.abspath(src)
    dst = path.abspath(dst)
    if not path.exists(src) or not path.isdir(src):
        raise Exception(f"{src} not exists or is not a directory")
    if not path.exists(dst):
        os.mkdir(dst)
    else:
        do_recursive(os.remove, [dst])
