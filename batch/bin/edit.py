#!/usr/bin/env python

import os
#import commands

import sys
import subprocess

#check = commands.getoutput("java -jar /home/ec2-user/git/validator/build/dist/vnu.jar http://www.sony.net/index.html")

# check = os.system('java -jar /home/ec2-user/git/validator/build/dist/vnu.jar /home/ec2-user/git/work/www.sony.co.jp/index.html')

#l = check.readline()
#logs = l.format(line)
#print (logs)
#print ('logs:{0}'.format(check))

#proc = subprocess.Popen("java -jar /home/ec2-user/git/validator/build/dist/vnu.jar http://www.sony.net/index.html", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
if len(sys.argv)<2 :
    print("File not assigned")
    sys.exit()
file = sys.argv[1]
if not os.path.exists(file) :
    print("No messages happen.")
    sys.exit()
fileobj = open(file)


buf = []
while True:
#    line = proc.stdout.readline()
    line = fileobj.readline()
    if not line:
        fileobj.close()
        break
    logs = ('{0}'.format(line))



    delimiter = '>"'
    index = -1
    index = logs.find(delimiter, index + 1)
    index1 = index
    delimiter = ':'
    index = logs.find(delimiter, index + 1)
    index = logs.find(delimiter, index + 1)
    index3 = index
    index = logs.find(delimiter, index + 1)
    index4 = index
    index0 = logs.__len__()


#    s = "id1:{ind1} id3:{ind3} id4:{ind4} id0:{ind0}"
#    text = s.format(ind1=index1, ind3=index3, ind4=index4, ind0=index0)
#    print (text)

    print logs[0:index1+1]
    print logs[index1+1:index3]
    print logs[index3+1:index4]
    print logs[index4+1:index0]
    print "--------------------------------------"
