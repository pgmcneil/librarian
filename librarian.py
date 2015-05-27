#!/usr/bin/env python3
"""
Usage:
    librarian.py --source=<source> --destination=<destination> [options]

Options:
    --catalog=<catalog>     Catalog file [Default: catalog.yaml]
    --dryrun                Don't actually do anything
    --delete                Delete the original after copying
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


def fillgroups(name, groups):
    '''Does a regex group substitution based on the regex groups'''
    for i in range(0, len(groups)):
        name = re.sub(r'\\{i}'.format(i=i + 1), groups[i], name)
    return name


def compare(name, catalog):
    '''Attempt to find the string in catalog'''
    for c in catalog.keys():
        item = catalog[c]
        try:
            t = item['target']
            # Support for multiple regex for item
            if isinstance(item['regex'], list):
                for r in item['regex']:
                    # See if we have a match
                    m = re.match(r, name, re.IGNORECASE)
                    if m:
                        # Go do a regex replace on the target string
                        t = fillgroups(t, m.groups())
                        return t
            elif isinstance(item['regex'], str):
                # See if we have a match
                m = re.match(item['regex'], name, re.IGNORECASE)
                if m:
                    # Go do a regex replace on the target string
                    t = fillgroups(t, m.groups())
                    return t
            else:
                raise TypeError("Needs to be a string or an array")
        except:
            raise Exception("Error processing item in catalog: {id}".format(id=c))
    return None


def deletefile(filename):
    try:
        if DRYRUN:
            print("Deleting {file}".format(file=filename))
        else:
            os.remove(filename)
    except:
        raise IOError("Error deleting file: {file}".format(file=filename))


def save(catalog):
    pass


def load(loadfile):
    try:
        with open(loadfile, 'r') as f:
            catalog = yaml.load(f)
        return catalog
    except:
        raise IOError("Error reading catalog file")


def scanandcopy(dir, catalog, dest, scandirs=False, delete=False):
    for root, dirs, files in os.walk(dir):
        for f in files:
            target = compare(f, catalog)
            if target:
                dest_folder = os.path.join(dest, target)
                abs_dest = os.path.join(dest_folder f)
                if DRYRUN:
                    print("Matched {file} copying to {dest}".format(file=f, dest=abs_dest))
                else:
                    # See if we need to make the final folder
                    if not path.exists(dest_folder):
                        os.mkdir(dest_folder)
                    shutil.copy(os.path.join(root, f), abs_dest)
                    # Double check it actually got copied
                    if not os.path.exists(abs_dest):
                        print("Failed to copy {file}".format(file=f))
                        delete = False
                if delete:
                    deletefile(os.path.join(root, f))

def main():
    global DRYRUN
    args = docopt(__doc__)
    catalog_file = args['--catalog']
    source_dir = args['--source']
    dest_dir = args['--destination']
    DRYRUN = args['--dryrun']
    delete = args['--delete']
    catalog = load(catalog_file)
    scanandcopy(source_dir, catalog, dest_dir, delete=delete)


if __name__ == "__main__":
    main()
