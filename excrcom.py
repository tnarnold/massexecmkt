#!/usr/bin/env python
'''
This runs a command on a bach of remote mikrotik routers using SSH. You need have installed
the paramiko library ("sudo pip install paramiko"). To use just put the IP Address of yours
hosts in the rtlist.txt each line one host, change the variables user and password on this file
and execute the fallowing command:
    python excrcom.py
author: Tiago Arnold <tiago@radaction.com.br>
'''
import paramiko
import sys

command='/ip address print'
user='admin'
password='tscpass'
port=22
hfh=open('rtlist.txt','r')
herr=open("err.txt",'a')
hdone=open("done.txt",'a')
herr.truncate()
hdone.truncate()
def sshCommand(hostname, port, username, password, command):
    try:
        sshClient = paramiko.SSHClient()
        sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        sshClient.load_system_host_keys()
        sshClient.connect(hostname, port, username, password,allow_agent=False,look_for_keys=False,timeout=3)
        stdin, stdout, stderr = sshClient.exec_command(command)
        hdone.write(hostname.strip()+" command result executed:\n")
        hdone.write(stdout.read()+"\n")
        sshClient.close()
        print(hostname.strip()+" command executed\n")
    except Exception as e:
        print(hostname.strip()+" - "+str(e)+"\n")
        herr.write(hostname.strip()+" - "+str(e).strip()+"\n")

if __name__ == '__main__':
    ips=hfh.readlines();
    for ip in ips:
        h=ip.split()
        sshCommand(h[0], port, user, password, command)
    herr.close()
    hdone.close()
    hfh.close()
