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
DATA_JSON_FILE_PATH = "_data/data.json"


def add_help_file(title: str, directory: str, filename: str, category: str):
    data.append(
        {
            "id": filename,
            "title": title,
            "url": f"https://{GITHUB_USERNAME}.github.io/{GITHUB_REPOSITORY}/{directory}/{filename}",
            "category": category,
        }
    )


def parse_markdown(path: str):
    with open(path) as md:
        metadata = frontmatter.load(md).metadata

    return metadata


def remove_preexisting_data():
    if os.path.exists(os.path.abspath("categories.json")):
        os.remove(os.path.abspath("categories.json"))

    if os.path.exists(os.path.abspath("data.json")):
        os.remove(os.path.abspath("data.json"))

    if os.path.exists(os.path.abspath("_data/categories.json")):
        os.remove(os.path.abspath("_data/categories.json"))

    if os.path.exists(os.path.abspath("_data/data.json")):
        os.remove(os.path.abspath("_data/data.json"))


if __name__ == "__main__":
    data = []

    remove_preexisting_data()

    directory_list = [
        directory
        for directory in next(os.walk("."))[1]
        if directory not in ("images", "Changelogs")
        and not directory.startswith("_")
        and not directory.startswith(".")
    ]

    for directory in directory_list:
        for file in os.listdir(os.path.abspath(directory)):
            help_file_frontmatter = parse_markdown(
                os.path.abspath(directory + "/" + file)
            )
            add_help_file(
                help_file_frontmatter["title"],
                directory,
                file.replace(".md", ""),
                help_file_frontmatter["category"],
            )

    if not os.path.isdir(os.path.abspath("_data")):
        os.mkdir("_data")

    with open(DATA_JSON_FILE_PATH, "w") as data_json:
        data_json.write(json.dumps(data, indent=4))