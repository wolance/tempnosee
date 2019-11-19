#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys
import datetime
import re

reano = r'(\/\*(\s|.)*?\*\/)|(\/\/.*)'

import os, sys,string,re,glob

Rule1 = "(\/\*(\s|.)*?\*\/)|(\/\/.*)"
c1=re.compile(Rule1)

def deal_file(src):
    if not os.path.exists(src):
        print 'Error: file - %s doesn\'t exist.'% src
        return False

    if os.path.islink(src):
        print 'Error: file - %s is a link.'
        return False

    filetype = (os.path.splitext(src))[1]
    if not filetype in ['.yar','.yara']:
        return False
    try:
        if not os.access(src, os.W_OK):
            os.chmod(src, 0664)
    except:
        print 'Error: you can not chang %s\'s mode.'% src

    inputf = open(src, 'r')
    outputfilename = (os.path.splitext(src))[0] + '_no_comment'+filetype
    outputf = open(outputfilename, 'w')
    lines=inputf.read()
    inputf.close()
    lines=re.sub(Rule1,"",lines)
    outputf.write(lines)
    outputf.close()
    return True

def print_files(rootpath, fp, path=''):
    if not len(path):
        path = rootpath
    lsdir = os.listdir(path)
    dirs = [i for i in lsdir if os.path.isdir(os.path.join(path, i))]
    if dirs:
        for i in dirs:
            print_files(rootpath, fp, os.path.join(path, i))
    files = [i for i in lsdir if os.path.isfile(os.path.join(path,i))]
    for f in files:
        if f[f.rfind('.'):] not in ['.yar', '.yara']:
            continue
        if f.find('vyara_') == 0:
            continue
        with open(path + os.sep + f, 'r') as tf:
            for line in tf:
                if re.match(r'rule [^=]', line):
                    print line,
                fp.write(line)


rootpath = 'D:\\Users\\dell\\Downloads\\rules-master\\yararule'
t = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
outfilename = rootpath + os.sep + 'vyara_%s.yar' % t
with open(outfilename, 'w+') as f:
    print_files(rootpath, f)

print 'over'
