Pylagiarist
===========

Pylagiarist is a plagiate detection script written in Python.

It recursively scans folders for files whose names match a certain
pattern, compares each pair of files, and reports those whose
similarity is beyond a given threshold.

Pylagiarist uses difflib's SequenceMatcher to compute similarities. If
[python-Levenshtein](https://github.com/ztane/python-Levenshtein/) is
installed, it also reports Levenshtein ratios for similar files.

Usage
-----

Just run

	pylagiarist.py

in the folder containing the files you want to compare. Pylagiarist
can take some switches, type

    pylagiarist.py -h

to learn about them.

Examples
--------

Scan folders `src1` and `src2` for files with names ending in `.html`
or `.htm`, but not matching `index`

	pylagiarist -i '.html$' -i '.htm$' -x index src1 src2

Report similarities above 0.4 (computed by difflib)

	pylagiarist -t 0.4

Print progress on stderr

	pylagiarist -v
