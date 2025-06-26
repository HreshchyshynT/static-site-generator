import utils


def main():
    utils.copy_files("./static", "./public")
    utils.generate_page("./content/index.md", "./template.html", "public/index.html")


if __name__ == "__main__":
    main()
