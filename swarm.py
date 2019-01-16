import paramiko
from paramiko import SSHClient
from scp import SCPClient
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from sqlite3 import Error

class Array:
    def __init__(self,name,mgmt=None,spa=None,spb=None):
        self.name = name
        self.spa = spa
        self.spb = spb
        self.mgmt = mgmt


    def insert_arrays_info(self):
        try:
            conn = sqlite3.connect('arrayTest.db')
            c = conn.cursor()
            c.execute("INSERT INTO arrays VALUES (?,?,?,?)",(self.name,self.mgmt,self.spa,self.spb))
            conn.commit()
        except Error as e:
            print(e)
        finally:
            conn.close()

    
    @staticmethod
    def get_arrayname(*data):
        val = "No data available"
        try:
            conn = sqlite3.connect('arrayTest.db')
            c = conn.cursor()
            array_name = c.execute(f"SELECT name FROM arrays WHERE {data[0]}=?",(data[1],))
            val = " ".join(a for a in array_name.fetchone()) 
        except Error as e:
            print(e)
        finally:
            conn.close()
            return val.strip()


    @staticmethod
    def data_exists(*data):
        val = False
        try:
            conn = sqlite3.connect('arrayTest.db')
            c = conn.cursor()
            output =  c.execute(f"SELECT * FROM arrays WHERE {data[0]}=?",(data[1],))
            if len(output.fetchall())>0:
                val = True
        except Error as e:
            print(e)
        finally:
            conn.close()
            return val





root = Tk()
root.title('Array Information')

def quitApplication(master=root):
    if messagebox.askquestion("Exit","Do you really want to quit the application?"):
        master.quit()


def swarm(master=root,arrayname=None,spa=None,spb=None,mgmt=None):
    arrayname = entry.get()
    mgmt = entry1.get()
    spa = entry2.get()
    spb = entry3.get()
    key = None
    val = None
    if arrayname or spa or  spb or mgmt:
        dbflag = False 
        array_name_flag = False
        print(len(arrayname),len(mgmt),len(spa),len(spb))
        if len(arrayname)>0:
                array_name_flag = True
                if  Array.data_exists('name',arrayname.upper().strip()):
                    print("Inside name")
                    key = 'name'
                    val = arrayname.upper().strip()
                    print(dbflag)
                    dbflag = True
                    print(dbflag)
        elif len(mgmt)>0:
                if  Array.data_exists('mgmt',mgmt.strip()):
                    print("inside mgmt")
                    key = 'mgmt'
                    val = mgmt.strip()
                    dbflag = True
        elif len(spa)>0:
                if  Array.data_exists('spa',spa.strip()):
                    print("inside spa")
                    key = 'spa'
                    val = spa.strip()
                    dbflag = True
        elif len(spb)>0:
                if  Array.data_exists('spb',spb.strip()):
                    print("inside spb")
                    key = 'spb'
                    val = spb.strip()
                    dbflag = True
        else:
                dbflag = False

        print(array_name_flag,dbflag)
        if array_name_flag or dbflag:     
            with SSHClient() as ssh:
                    ssh.load_system_host_keys()
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    ####Enter the host info and connect via ssh####
                    ##i.essh.connect("xx.xxx.xxx.xxx",22,username="Admin",password="Password",sock=None)
                    if dbflag and not array_name_flag:
                        arrayname = Array.get_arrayname(key,val)
                    command = f"swarm {arrayname.upper().strip()}"
                    print(command)
                    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command)
                    err = "".join(ssh_stderr.readlines())
                    if err:
                        op =  err
                    else:
                        op = "".join(ssh_stdout.readlines()).strip()
                        print(dbflag)
                        if  dbflag == False:
                            print("Inserting data into db")
                            name = op[op.find("Name:")+len("Name:")+1:op.find("Name:")+len("Name:")+9].strip()
                            mgmt_ip = op[op.find("Mgmt IP:")+len("Mgmt IP:")+1:op.find("Mgmt IP:")+len("Mgmt IP:")+16].strip()
                            spa_ip = op[op.find("Lab IP SPA:")+len("Lab IP SPA:")+1:op.find("Lab IP SPA:")+len("Lab IP SPA:")+16].strip()
                            spb_ip = op[op.find("Lab IP SPB:")+len("Lab IP SPB:")+1:op.find("Lab IP SPB:")+len("Lab IP SPB:")+16].strip()
                            data = Array(name,mgmt_ip,spa_ip,spb_ip)
                            data.insert_arrays_info()
                            print("name"+" "+name)
                            print("mgmt"+" "+mgmt_ip)
                            print("spa"+" "+spa_ip)
                            print("spb"+" "+spb_ip)
                    
                    print(err)
                    text.configure(state='normal')
                    text.delete(1.0,END)
                    text.insert(1.0,op)
                    text.configure(state='disabled') 
        else:
                text.configure(state='normal')
                text.delete(1.0,END)
                text.insert(1.0,"You have to enter the Array name !!!")
                text.configure(state='disabled')                      
    else:
        text.configure(state='normal')
        text.delete(1.0,END)
        text.insert(1.0,"No information is provided regarding the array")
        text.configure(state='disabled')
    entry.delete(0, 'end')
    entry1.delete(0, 'end')
    entry2.delete(0, 'end')
    entry3.delete(0, 'end')









root.geometry("800x600+350+100")
array_name = Label(root,text = "Enter the name of the array ")
array_name.pack()
entry = Entry()
entry.pack()

text = entry.get()

mgmt = Label(root,text = "CS IP Address -  ")
mgmt.pack()
entry1 = Entry()
entry1.pack()

spa = Label(root,text = "SPA IP Address -  ")
spa.pack()
entry2 = Entry()
entry2.pack()

spb = Label(root,text = "SPB IP Address -  ")
spb.pack()
entry3 = Entry()
entry3.pack()



click = Button(root,text="click here",bg="cyan",command=swarm)
click.pack()
exiting = Button(root,text="Exit",bg="cyan",command=quitApplication)
exiting.pack()

frame = Frame(root, bd=2, relief=SUNKEN)
frame.pack()
frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)

xscrollbar = Scrollbar(frame, orient=HORIZONTAL)
xscrollbar.grid(row=1, column=0, sticky=E+W)

yscrollbar = Scrollbar(frame)
yscrollbar.grid(row=0, column=1, sticky=N+S)

text = Text(frame, wrap=NONE, bd=0,
                        xscrollcommand=xscrollbar.set,
                        yscrollcommand=yscrollbar.set,height=600,width=800)

text.grid(row=0, column=0, sticky=N+S+E+W)

xscrollbar.config(command=text.xview)
yscrollbar.config(command=text.yview)






root.mainloop()
