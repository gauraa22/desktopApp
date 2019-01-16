import paramiko
from paramiko import SSHClient
from scp import SCPClient
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
 
 

with SSHClient() as ssh:        
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("10.244.192.215",22,username="root",password="c4dev!",sock=None)
    command = f"swarm JF-D1299"
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command)
    err = "".join(ssh_stderr.readlines())
    if err:
            op =  err
    else:
            op = "".join(ssh_stdout.readlines()).strip()

    name = op[op.find("Name:")+len("Name:")+1:op.find("Name:")+len("Name:")+9].strip()
    mgmt_ip = op[op.find("Mgmt IP:")+len("Mgmt IP:")+1:op.find("Mgmt IP:")+len("Mgmt IP:")+16].strip()
    spa_ip = op[op.find("Lab IP SPA:")+len("Lab IP SPA:")+1:op.find("Lab IP SPA:")+len("Lab IP SPA:")+16].strip()
    spb_ip = op[op.find("Lab IP SPB:")+len("Lab IP SPB:")+1:op.find("Lab IP SPB:")+len("Lab IP SPB:")+16].strip()
    print("name"+" "+name)
    print("mgmt"+" "+mgmt_ip)
    print("spa"+" "+spa_ip)
    print("spb"+" "+spb_ip)
    ssh.connect("10.244.192.215",22,username="root",password="c4dev!",sock=None)



