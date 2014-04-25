#!/usr/bin/python

from optparse import OptionParser
from difflib import SequenceMatcher
import sys, os, os.path
import re
try:
    import Levenshtein as lev
except ImportError:
    lev = None

parser = OptionParser(usage='%prog [OPTION]... [PATH]...',
                      description='Compare files in PATH for plagiarism')
parser.add_option('-i', '--include', action='append', metavar='PATTERN',
                  help='include files matching pattern')
parser.add_option('-x', '--exclude', action='append', metavar='PATTERN',
                  help='exclude files matching pattern')
parser.add_option('-t', '--threshold', type='float',
                  metavar='[0,1]', default=0.7,
                  help='notify above this similarity ratio (default 0.7)')
parser.add_option('-v', '--verbose', action='store_true',
                  help='print progress information to stderr')

options, args = parser.parse_args()

if (not args):
    args = ['.']

filelist = []
for path in args:
    if os.path.isdir(path):
        for dirpath, _, filenames in os.walk(path):
            for f in filenames:
                filelist.append(os.path.join(dirpath, f))
    elif os.path.isfile(path):
        filelist.append(path)
    else:
        exit('%s: Cannot open %s' % (os.path.basename(sys.argv[0]), path))


filelist = filter(lambda f : 
                  (not options.include or
                   any(re.search(p, f) for p in options.include)) and
                  (not options.exclude or
                   not any(re.search(p, f) for p in options.exclude)),
                  filelist)

if options.verbose:
    sys.stderr.write('Comparing %d files in %s ...\n' % (len(filelist), ', '.join(args)))

count = 0.0
itotal = 2.0 / ((len(filelist)-1)*len(filelist))
e = 1 + (len(filelist) > 50)
while filelist:
    a = filelist.pop()
    atext = open(a).read()
    for b in filelist:
        old = round(count, e)
        count += itotal
        if options.verbose and old != round(count, e):
            sys.stderr.write('%d%%\r' % int(old*100))

        btext = open(b).read()
        sm1 = SequenceMatcher(a=atext, b=btext)
        sm2 = SequenceMatcher(a=btext, b=atext)
        if any((sm.real_quick_ratio() >= options.threshold
                and sm.quick_ratio() >= options.threshold
                and sm.ratio() >= options.threshold)
               for sm in (sm1, sm2)):
            print '''
Possible plagiarism: difflib %f, %f%s.
    %s
    %s''' % (sm1.ratio(), sm2.ratio(),
             ', Levenshtein %f' % lev.ratio(a,b) if lev else '',
             a, b)
