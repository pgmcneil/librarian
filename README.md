## Librarian
Librarian is a simple python script that can read in a yaml catalog of items, scan a directory for files matching the regex in the catalog, and then copy the files to a destination. Useful for curating a directory and automatically copying files off to a different location.

### Usage:
Basic usage is as follows:

```
$ ./librarian.py -h
Usage:
    librarian.py --source=<source> --destination=<destination> [options]

Options:
    --catalog=<catalog>     Catalog file [Default: catalog.yaml]
    --dryrun                Don't actually do anything
    -h --help               Show help
```

### ToDo:
1. Add support for moving files
2. Add support for entire directories, most likely a flag in the catalog too
3. Add support for deleting source files
..* MD5/SHA1/SHA256 checksum before deleting?
