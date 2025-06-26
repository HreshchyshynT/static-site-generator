import utils
import sys


def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    utils.copy_files("./static/", "./docs/")
    utils.generate_page_recursive(
        basepath,
        "./content/",
        "./template.html",
        "./docs/",
    )


if __name__ == "__main__":
    main()
