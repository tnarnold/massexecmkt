
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

command="/interface ethernet print"
user="admin"
password="senha"

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
        herr.write(ip.strip()+" host not found\n")
        error=ssh.stderr.readlines()
        print >> sys.stderr,"ERROR: %s"% error
    elif result[1].find("password")>-1:
        herr.write(ip.strip()+" password invalid\n")
        error=ssh.stderr.readlines()
        print >> sys.stderr,"ERROR: %s"% error
    else:
        hdone.write(ip.strip()+" command result executed:\n")
        result.pop(0)
        result.pop(len(result)-1)
        print(result)
        for l in result:
            print(l.strip())
            hdone.write("    "+l.strip()+"\n")
        hdone.write("\n")

herr.close()
hdone.close()
