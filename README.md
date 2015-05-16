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

### Features
* Full regex supported catalog (yaml)
* Support for regex group matching (see examples)
* Support for file deletions after completion


### Examples
#### Basic usage
Sample catalog.yaml
```
---
test1:
  target: 'test_folder'
  regex: 'testing_\d'
different:
  target: 'diff/sub'
  regex: '.*different.+'
```
And the directory structure
```
.
├── after
│   ├── diff
│   │   └── sub
│   └── test_folder
└── before
    ├── dasdf
    ├── different_file
    ├── testing_1
    ├── testing_2
    └── testing3
```
And the script output in dryrun mode to view what it is doing. Notice that
the file testing3 and dasdf are ignored because they do not match anything in
the catalog.
```
$ ./librarian.py --source ~/tmp/before --destination ~/tmp/after --dryrun
Matched testing_1 copying to /home/pgmcneil/tmp/after/test1_folder/testing_1
Matched testing_2 copying to /home/pgmcneil/tmp/after/test2_folder/testing_2
Matched different_file copying to /home/pgmcneil/tmp/after/diff/sub/different_file
```

#### Regex group matching
Using the same example as above but let's say we want finer control. Using
some of the example above:
Sample catalog.yaml
```
---
test1:
  target: 'test\1_folder'
  regex: 'testing_(\d)'
```
And the directory structure:
```
.
├── after
│   └── test1_folder
│   └── test2_folder
└── before
    ├── testing_1
    ├── testing_2
```
And the dryrun output of the script. Notice how the number for the file was
replaced in the folder name using the group matching notation of \1.
```
$ ./librarian.py --source ~/tmp/before --destination ~/tmp/after --dryrun
Matched testing_1 copying to /home/pgmcneil/tmp/after/test1_folder/testing_1
Matched testing_2 copying to /home/pgmcneil/tmp/after/test2_folder/testing_2
```


### ToDo:
1. Add support for moving files
2. Add support for entire directories, most likely a flag in the catalog too
3. MD5/SHA1/SHA256 checksum before deleting?
