#!/usr/bin/env python3
"""
Usage:
    librarian.py --source=<source> --destination=<destination> [options]

Options:
    --catalog=<catalog>     Catalog file [Default: catalog.yaml]
    --dryrun                Don't actually do anything
    -h --help               Show help
"""

from docopt import docopt
import yaml
import re
import shutil
import os

# Globals
DRYRUN = False
# End globals


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
                    return item['target']
            else:
                raise TypeError("Needs to be a string or an array")
        except:
            raise KeyError("Malformed object in catalog: {id}".format(id=c))
    return None


def save(catalog):
    pass


def load(loadfile):
    try:
        with open(loadfile, 'r') as f:
            catalog = yaml.load(f)
        return catalog
    except:
        raise IOError("Error reading catalog file")


def scanandcopy(dir, catalog, dest, scandirs=False):
    for root, dirs, files in os.walk(dir):
        for f in files:
            if compare(f, catalog):
                if DRYRUN:
                    print("Matched {file} copying to {dest}".format(file=f, dest=os.path.join(dest, f)))
                else:
                    shutil.copy(os.path.join(root, f), os.path.join(dest, f))

def main():
    global DRYRUN
    args = docopt(__doc__)
    catalog_file = args['--catalog']
    source_dir = args['--source']
    dest_dir = args['--destination']
    DRYRUN = args['--dryrun']
    catalog = load(catalog_file)
    scanandcopy(source_dir, catalog, dest_dir)


if __name__ == "__main__":
    main()
