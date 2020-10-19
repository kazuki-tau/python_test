#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3
# coding:utf-8

import sys
import os
import datetime as dt
import time
import subprocess
import re

#pid取得
pid = os.getpid()

#引数確認
args = sys.argv
if len(args) != 2:
    print("引数が不正です",file=sys.stderr)
    sys.exit(2)

#ファイル読み込み
try:
    file = open(args[1],'r')
except FileNotFoundError as e:
    print('ファイルが存在しません', file=sys.stderr)
    sys.exit(1)
except PermissionError as e:
    print('ファイルを開く権限がありません', file=sys.stderr)
    sys.exit(1)
readlines = file.readlines()

#書き出しファイル

output_file_name = 'output.' + str(pid) + '.txt'
try:
    output_file = open(output_file_name,'x')

except FileExistsError as e:
    print('すでにファイルが存在しています。',file=sys.stderr)
    sys.exit(1)

#全て空行か確認
pattern = re.compile(r'^(\s)+$')
check_list = [i for i in readlines if re.match(pattern,i) == None]
if len(check_list) == 0:
    print('全て空行です',file=sys.stderr)
    sys.exit(1)

for i in readlines:
    if re.match(pattern,i) == None:
        t = dt.datetime.now()
        line = t.strftime('%Y/%m/%d %H-%M-%S:') + str(time.time()) + ':' + i
        output_file.writelines(line)

file.close()
output_file.close()

cmd = subprocess.run("ls -l",shell=True)
if cmd.returncode != 0:
    print('コマンドが失敗しました。',file=sys.stderr)
    sys.exit(1)
sys.exit(0)
