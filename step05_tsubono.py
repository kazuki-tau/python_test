#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3
# coding:utf-8

import sys
import paramiko
import datetime


args = sys.argv
if len(args) < 2:
    print('読み込むファイルを指定してください')
try:
    file = open(args[1],'r')
except FileExistsError as a:
    print('ファイルが存在しません。',file=sys.stderr)
    sys.exit(1)
except PermissionError as e:
    print('ファイルを開く権限がありません。', file=sys.stderr)


lines = file.readlines()
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

for i in op:
    # print('!!!!!!!!!!!!!')
    # print(f'{count}行目です')
    # print(i[3])
    client = paramiko.SSHClient()
    # client.load_host_keys('./known_hosts')
    # client.set_missing_host_key_policy(paramiko.WarningPolicy)
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    match = False
    try:
        if i[0] == '' and i[1] == '' and i[2] == '':
            address,user,password = last_login_address,last_login_user,last_login_password
        else:
            address, user, password = i[0], i[1], i[2]
        client.connect(address,username=user,password=password,timeout=5)
        time = datetime.datetime.now()
        stdin, stdout,stderr = client.exec_command(i[3])
        out = []
        for j in stdout:

            word = i[4].replace('\n','')
            if word in j:
                match = True
            out.append(j)

            # if stderr:
            #     for z in stderr:
            #         print('!!!!!!!!!!!!!!!!!!!!!!!error!!!!!!!!!!!!!')
            #         print(z)
        print('================================')
        print(f'IPアドレス:{address}')
        print(f'ログインユーザー:{user}')
        print(f'実行時刻:{time}')
        print(f"結果:{'OK' if match == True else 'NG'} ({word})")
        print('================================')
        print('実行結果↓')
        print('\n')
        for o in out:
            print(o.replace('\n',''))

        last_login_address, last_login_user, last_login_password = i[0], i[1], i[2]
    except Exception as e:
        print(e)
        print('ssh接続に失敗しました。')
        sys.exit(1)


    client.close()
sys.exit(0)


