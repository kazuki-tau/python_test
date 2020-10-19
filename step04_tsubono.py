#! /Library/Frameworks/Python.framework/Versions/3.6/bin/python3
# coding:utf-8

import sys
import os
import re

args = sys.argv
if len(args) < 3:
    print('引数が3つ未満です。',file=sys.stderr)
    sys.exit(1)

file = open(args[1],'r')

file.close()