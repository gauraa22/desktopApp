import paramiko
from paramiko import SSHClient
from scp import SCPClient
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from sqlite3 import Error

class Array:
    def __init__(self,name,mgmt,spa,spb):
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
    def data_exists(*data):
        val = False
        try:
            conn = sqlite3.connect('arrayTest.db')
            c = conn.cursor()
            if c.execute(f"SELECT * FROM arrays WHERE {data[0]}=?",(data[1],)):
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
    spa = entry1.get()
    flag = False
    if arrayname or spa or  spb or mgmt: 
        if len(arrayname)>0:
            if  Array.data_exists('name',arrayname.upper()):
                flag = True
        with SSHClient() as ssh:
            ssh.load_system_host_keys()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect("10.244.192.215",22,username="root",password="c4dev!",sock=None)
            command = f"swarm {arrayname.upper().strip()}"
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command)
            err = "".join(ssh_stderr.readlines())
            if err:
                op =  err
            else:
                op = "".join(ssh_stdout.readlines()).strip()
            
            print(err)
            text.configure(state='normal')
            text.delete(1.0,END)
            text.insert(1.0,op)
            text.configure(state='disabled')
                    
    else:
        text.configure(state='normal')
        text.delete(1.0,END)
        text.insert(1.0,"No information is provided regarding the array")
        text.configure(state='disabled')










root.geometry("800x600+350+100")
array_name = Label(root,text = "Enter the name of the array ")
array_name.pack()
entry = Entry()
entry.pack()

text = entry.get()

spa = Label(root,text = "SPA IP Address -  ")
spa.pack()
entry1 = Entry()
entry1.pack()



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
