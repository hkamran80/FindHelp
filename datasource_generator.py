"""
Data Source Generator
Contributors:
    :: H. Kamran [@hkamran80] (author)
Version: 1.0.0
Last Updated: 2020-10-09, @hkamran80
"""

import frontmatter
import json
import os

GITHUB_USERNAME = os.environ.get("GITHUB_ACTOR")
GITHUB_REPOSITORY = os.environ.get("GITHUB_REPOSITORY").split("/")[1]


def add_help(title: str, directory: str, filename: str, md_categories: list):
    for category in md_categories:
        try:
            categories[category].append(filename)
        except KeyError:
            categories[category] = [filename]

    data[filename] = {
        "title": title,
        "url": f"https://{GITHUB_USERNAME}.github.io/{GITHUB_REPOSITORY}/{directory}/{filename}",
        "categories": md_categories,
    }


def parse_markdown(path: str):
    with open(path) as md:
        metadata = frontmatter.load(md).metadata

    metadata["category"] = metadata["category"].split(",")

    return metadata


if __name__ == "__main__":
    data = {}
    categories = {}

    directory_list = [
        directory
        for directory in next(os.walk("."))[1]
        if directory not in ("images", "Changelogs")
        and not directory.startswith("_")
        and not directory.startswith(".")
    ]

    for directory in directory_list:
        for file in os.listdir(os.path.abspath(directory)):
            fm = parse_markdown(os.path.abspath(directory + "/" + file))
            add_help(fm["title"], directory, file.replace(".md", ""), fm["category"])

    with open("data.json", "w") as data_json:
        data_json.write(json.dumps(data, indent=4))

    with open("categories.json", "w") as categories_json:
        categories_json.write(json.dumps(categories, indent=4))