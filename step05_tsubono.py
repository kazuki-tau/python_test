#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3
# coding:utf-8

import sys
import paramiko
import datetime
import re

args = sys.argv
#引数二以下はエラー
if len(args) < 2:
    print('読み込むファイルを指定してください')
#引数で与えられたファイルの確認
try:
    file = open(args[1],'r')
except FileExistsError as a:
    print('ファイルが存在しません。',file=sys.stderr)
    sys.exit(1)
except PermissionError as e:
    print('ファイルを開く権限がありません。', file=sys.stderr)

lines = file.readlines()

#空行チェック
pattern = re.compile('^(\s)+$')
check_list = [i for i in lines if re.match(pattern,i) == None]
if len(check_list) == 0:
    print('ファイルの中身が全て空行です',file=sys.stderr)
    sys.exit(1)

#csvから以下のlistを作成
#op = [[ip_address1, usename1, passowrd1, command1, matchPattern1],[ip_address2, usename2, passowrd2,command2, matchPattern2],...]
op = [i.split(',') for i in lines]

# client = paramiko.SSHClient()
# client.load_host_keys('./known_hosts')
# client.set_missing_host_key_policy(paramiko.WarningPolicy)
# client.connect('localhost',username='null',password='A1276162')
# stdin,stdout,stderr = client.exec_command('netstat -rn')
#
# l = []
# for i in stdout:
#     l.append(i.replace('\n',''))
#     print(i.replace("\n",''))
# client.close()
# print(op)

#書き出しファイル
file_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
output_file_name = 'out.' + file_time + '.txt'
try:
    output_file = open(output_file_name,'x')
except FileExistsError as e:
    print('すでにファイルが存在しています。',file=sys.stderr)
    sys.exit(1)

#ssh接続
for i in op:
    client = paramiko.SSHClient()
    # client.load_host_keys('./known_hosts')
    # client.set_missing_host_key_policy(paramiko.WarningPolicy)
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    match = False
    #,,,command,wordの場合,前回使用した接続を使う
    try:
        if i[0] == '' and i[1] == '' and i[2] == '':
            address,user,password = last_login_address,last_login_user,last_login_password
    #ipaddress,username,password,command,wordの場合
        else:
            address, user, password = i[0], i[1], i[2]
        #5秒接続できなかったら、timeout
        client.connect(address,username=user,password=password,timeout=5)
        time = datetime.datetime.now()
        stdin, stdout,stderr = client.exec_command(i[3])
        #out: command結果をfileに出力するようのlist
        out = []
        for j in stdout:
            word = i[4].replace('\n','')
        #command結果を各行ごとに、検索wordがあるかcheck
            if word in j:
                match = True
            out.append(j)

        # if stderr:
        #      for z in stderr:
        #         print(z,file=output_file)
        #結果をoutput_fileに書き出し
        print('================================',file=output_file)
        print(f'IPアドレス:{address}',file=output_file)
        print(f'ログインユーザー:{user}',file=output_file)
        print(f'実行時刻:{time}',file=output_file)
        print(f"結果:{'OK' if match == True else 'NG'} (検索ワード:{word})",file=output_file)
        print('================================',file=output_file)
        print('実行結果↓',file=output_file)
        print('\n',file=output_file)
        if len(out) > 1:
            for o in out:
                print(o.replace('\n',''),file=output_file)
        if stderr:
            print('!!!!!!!!!!!error!!!!!!!!!!!', file=output_file)
            for z in stderr:
                print(z, file=output_file)
        #最後に接続したsshの情報を変数に格納
        last_login_address, last_login_user, last_login_password = i[0], i[1], i[2]
    except Exception as e:
        print(e)
        print('ssh接続に失敗しました。',file=output_file)
        print(f'{i}をスキップします',file=output_file)


    client.close()
output_file.close()
sys.exit(0)


