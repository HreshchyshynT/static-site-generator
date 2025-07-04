from os import path as path
import os
import shutil
from markdown_block import markdown_to_html_node
from inline_markdown import extract_title


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

    def copy(file):
        dst_file = file.replace(src, dst)
        dir = path.dirname(dst_file)
        if not path.exists(dir):
            os.mkdir(dir)
        shutil.copy(file, dst_file)

    do_recursive(copy, [src])


def generate_page(
    basepath,
    from_path,
    template_path,
    dest_path,
):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    from_path = path.abspath(from_path)
    template_path = path.abspath(template_path)
    dest_path = path.abspath(dest_path)
    with open(from_path) as f:
        md = f.read()
    with open(template_path) as f:
        template = f.read()

    html = markdown_to_html_node(md).to_html()
    title = extract_title(md)
    template = (
        template.replace("{{ Title }}", title)
        .replace("{{ Content }}", html)
        .replace('href="/', f'href="{basepath}')
        .replace('src="/', f'src="{basepath}')
    )

    if not path.exists(path.dirname(dest_path)):
        os.makedirs(path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(template)


def generate_page_recursive(
    basepath,
    dir_path_content,
    template_path,
    dest_dir_path,
):
    def do_recursive(what, all, parent=""):
        for file in all:
            p = path.join(parent, file)
            if path.isdir(p):
                do_recursive(what, os.listdir(p), parent=p)
            else:
                what(p)

    def generate_file(f):
        if not f.endswith(".md"):
            return
        dest = f.replace(dir_path_content, dest_dir_path).replace(".md", ".html")
        generate_page(basepath, f, template_path, dest)

    do_recursive(generate_file, [dir_path_content])
