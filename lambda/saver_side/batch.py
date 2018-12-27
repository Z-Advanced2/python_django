#!/usr/bin/env python3

#import os
#import commands

import sys
import subprocess
import re
import datetime

# Check path between account management path to validate path
# It is not fixed to return error code to lambda
# If it matced then fix path for result
args = sys.argv
print(args[1])

now = datetime.datetime.now()
print(str(now))

acc_path = '/nouhin/acc_info/acclist.dat'
reqpath = args[1]
scnt = reqpath.count('/') - 3
print(scnt)
AA = reqpath.rsplit("/",scnt)
print(AA[0])
editpath = AA[0]
with open(acc_path) as a:
    acc = a.read()
MO = re.search(editpath, acc)
print(MO)
if str(MO) in "None" :
    print("Not subject to processing")
    exit()
#if reqpath[-1] != "/" :

BB = reqpath.split("/", 5)

resultfile = '{0:%Y%m%d_%I%M%S}_'.format(now) + BB[-1].replace('/', '_')
outpath = editpath + '/fromSony/validated/' + resultfile
with open(outpath, mode='w') as f:

#check = commands.getoutput("java -jar /home/ec2-user/git/validator/build/dist/vnu.jar http://www.sony.net/index.html")

# check = os.system('java -jar /home/ec2-user/git/validator/build/dist/vnu.jar /home/ec2-user/git/work/www.sony.co.jp/index.html')

#l = check.readline()
#logs = l.format(line)
#print (logs)
#print ('logs:{0}'.format(check))

    proc = subprocess.Popen("java -jar /home/ec2-user/git/validator/build/dist/vnu.jar --skip-non-html " + args[1], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    buf = []
    while True:
        line = proc.stdout.readline()
        if not line:
            break
        logs = ('logs:{0}'.format(line))



        delimiter = ':'
        index = -1
        index = logs.find(delimiter, index + 1)
        index1 = index
        index = logs.find(delimiter, index + 1)
        index = logs.find(delimiter, index + 1)
        index3 = index
        index = logs.find(delimiter, index + 1)
        index4 = index
        index0 = logs.__len__()


#    s = "id1:{ind1} id3:{ind3} id4:{ind4} id0:{ind0}"
#    text = s.format(ind1=index1, ind3=index3, ind4=index4, ind0=index0)
#    print (text)

        print(logs[0:index1])
        f.writelines ('\n' + logs[0:index1])
        print(logs[index1+3:index3])
        f.writelines ('\n' + logs[index1+1:index3])
        print(logs[index3+1:index4])
        f.writelines ('\n' + logs[index3+1:index4])
# UTF-8's start" end" change to ascii " and ommit cr
        print(logs[index4+1:index0].replace('\\xe2\\x80\\x9c','"').replace('\\xe2\\x80\\x9d','"').replace('\\n',''))
        f.writelines ('\n' + logs[index4+1:index0])
        print("-------------------------------------------------")
