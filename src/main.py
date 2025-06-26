import utils


def main():
    utils.copy_files("./static", "./public")
    utils.generate_page("./content/index.md", "./template.html", "public/index.html")
    utils.generate_page(
        "./content/blog/glorfindel/index.md",
        "./template.html",
        "public/blog/glorfindel/index.html",
    )
    utils.generate_page(
        "./content/blog/tom/index.md",
        "./template.html",
        "public/blog/tom/index.html",
    )
    utils.generate_page(
        "./content/blog/majesty/index.md",
        "./template.html",
        "public/blog/majesty/index.html",
    )
    utils.generate_page(
        "./content/contact/index.md", "./template.html", "public/contact/index.html"
    )


if __name__ == "__main__":
    main()
