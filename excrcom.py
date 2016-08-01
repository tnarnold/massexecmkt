
#!/usr/bin/env python

'''

This runs a command on a bach of remote mikrotik routers using SSH. You need have installed
the expect tcl/tk interpreter on linux to this works. To use just put the IP Address of
hosts in the rtlist.txt each line one host, change the variables user and password on this file
and execute the fallowing command:

    python excrcom.py

author: Tiago Arnold <tiago@radaction.com.br>

'''

import subprocess as sub
import sys

command="/system reboot"
user="admin"
password="tscpass"

handle = open("rtlist.txt",'r')
herr=open("err.txt",'a')
hdone=open("done.txt",'a')

ips=handle.readlines();

herr.truncate()
hdone.truncate()

for ip in ips:
    ssh = sub.Popen(["expect","conrt.exp",ip,user,password,command],shell=False,stdout=sub.PIPE,stderr=sub.PIPE)
    result =ssh.stdout.readlines()
    if  result == []:
        herr.write(ip.strip()+" password error or host not found\n")
    else:
        hdone.write(ip.strip()+" command result executed:\n")
        result.pop(0)
        result.pop(len(result)-1)
        for l in result:
            print(l.strip())
            hdone.write("    "+l.strip()+"\n")
        hdone.write("\n")

herr.close()
hdone.close()
