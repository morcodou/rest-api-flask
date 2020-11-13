"""
libs.strings

By default, uses en-gb.json file inside the strings  top folder

"""

import json

default_locale = "en-gb"
cached_strings = {}


def refresh():
    global cached_strings
    with open(f"strings/{default_locale}.json") as f:
        cached_strings = json.load(f)


def gettext(name: str) -> str:
    return cached_strings[name]


refresh()
