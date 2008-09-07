#!/usr/bin/python

import sys
import os
import os.path
import re
import md5
import tempfile
import cPickle
from getopt import getopt

opt_use_modtime = False
opt_dirs = ['.']
opt_show_up_to_date = True

def set_use_modtime(use):
    global opt_use_modtime
    opt_use_modtime = use

def set_show_up_to_date(show):
    global opt_show_up_to_date
    opt_show_up_to_date = show

def add_relevant_dir(d):
    opt_dirs.append(d)

def md5sum(fname):
    try: data = file(fname).read()
    except: data = None

    if data == None: return 'nonexistent'
    else: return md5.new(data).hexdigest()

def modtime(fname):
    try: return os.path.getmtime(fname)
    except: return 'nonexistent'

def files_up_to_date(files):
    for (fname, md5, mtime) in files:
        if opt_use_modtime:
            if modtime(fname) <> mtime:
                print '(File %s has changed)' % fname
                return False
        else:
            if md5sum(fname) <> md5:
                print '(File %s has changed)' % fname
                return False
    return True

def is_relevant(fname):
    path1 = os.path.abspath(fname)
    for d in opt_dirs:
        path2 = os.path.abspath(d)
        if path1.startswith(path2): return True
    return False

# NOTE: One possible problem is that the program output depends
# on whether a directory exists or not, or on the contents
# of a directory.

def generate_deps(cmd):
    print 'running', cmd

    ecmd = cmd
    ecmd = ecmd.replace('\\', '\\\\')
    ecmd = ecmd.replace('"', '\\"')

    outfile = tempfile.mktemp()
    calls = 'open,stat64,execve,exit_group'
    r = os.system('strace -f -o %s -e trace=%s /bin/sh -c "%s"'
                  % (outfile, calls, ecmd))
    if r != 0: return (r, [])
    output = file(outfile).readlines()
    os.remove(outfile)

    status = 0
    files = []
    files_dict = {}
    for line in output:
        match1 = re.match(r'.*open\("([^"]*)", .*', line)
        match2 = re.match(r'.*stat64\("([^"]*)", .*', line)
        match3 = re.match(r'.*execve\("([^"]*)", .*', line)
        match4 = re.match(r'.*killed by.*', line)

        if match4: return (2, [])

        if match1: match = match1
        elif match2: match = match2
        else: match = match3
        if match:
            fname = os.path.normpath(match.group(1))
            if (is_relevant(fname)
                and (os.path.isfile(fname) or not os.path.lexists(fname))
                and not files_dict.has_key(fname)):
                files.append((fname, md5sum(fname), modtime(fname)))
                files_dict[fname] = True

        match = re.match(r'.*exit_group\((.*)\).*', line)
        if match: status = int(match.group(1))

    return (status, files)

def read_deps(depsname):
    try: f = file(depsname, 'rb')
    except: f = None

    if f:
        deps = cPickle.load(f)
        f.close()
        return deps
    else:
        return {}

def write_deps(depsname, deps):
    f = file(depsname, 'wb')
    cPickle.dump(deps, f)
    f.close()

def memoize_with_deps(depsname, deps, cmd):
    files = deps.get(cmd, None)
    if files == None or not files_up_to_date(files):
        (status, files) = generate_deps(cmd)
        if status == 0: deps[cmd] = files
        elif deps.has_key(cmd): del deps[cmd]
        write_deps(depsname, deps)
        return status
    else:
        if opt_show_up_to_date: print 'up to date:', cmd
        return 0

default_depsname = '.deps'
default_deps = read_deps(default_depsname)

def memoize(cmd):
    return memoize_with_deps(default_depsname, default_deps, cmd)

if __name__ == '__main__':
    (opts, cmd) = getopt(sys.argv[1:], 'td:')
    cmd = ' '.join(cmd)
    for (opt, value) in opts:
        if opt == '-t': opt_use_modtime = True
        elif opt == '-d': opt_dirs.append(value)

    status = memoize(cmd)
    sys.exit(status)
