#!/usr/bin/env python3
"""
Usage:
    librarian.py [options]

Options:
    --catalog=<catalog>     Catalog file [Default: catalog.yaml]
    -h --help               Show help
"""

from docopt import docopt
import yaml
import re

# Globals
catalog_file = None
catalog = None
# End


def compare(name, catalog):
    for c in catalog.keys():
        item = catalog[c]
        try:
            if isinstance(item['regex'], list):
                for r in item['regex']:
                    if re.match(r, name, re.IGNORECASE):
                        return item['title']
            elif isinstance(item['regex'], str):
                if re.match(item['regex'], name, re.IGNORECASE):
                    return item['title']
            else:
                raise TypeError("Needs to be a string or an array")
        except:
            raise KeyError("No index 'regex'")
    return None


def save(catalog):
    pass


def load():
    try:
        with open(catalog_file, 'r') as f:
            catalog = yaml.load(f)
        return catalog
    except:
        raise IOError("Error reading catalog file")


def main():
    global catalog
    catalog = load()


if __name__ == "__main__":
    global config
    args = docopt(__doc__)
    catalog_file = args['--catalog']
    main()
