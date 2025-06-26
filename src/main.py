import utils


def main():
    utils.copy_files("./static/", "./public/")
    utils.generate_page_recursive("./content/", "./template.html", "./public/")


if __name__ == "__main__":
    main()
