# -*- coding: cp1251 -*-
from omniORB import CORBA
import sqlite3, os, sys
from Tkinter import *
import ttk
import tkMessageBox
import tkFileDialog
from tables import CreateTable
import _GlobalIDL


def Client():  
    tkMessageBox.showinfo('Ok', "Congratulations! You are able to connect to server now! Check the console")

    for i in c.execute("SELECT * FROM Dll WHERE MotherWell='" + tree.selection()[0][2:] + "'"):
        with open(i[2]) as f:
            L = f.readlines()
            for i in xrange(2,len(L)):
                lb.insert(i, L[i])
        
    orb = CORBA.ORB_init(sys.argv, CORBA.ORB_ID)
    #obj = orb.string_to_object(raw_input("Enter IOR here:"))
    with open("D:/ior.txt") as f:
        obj = orb.string_to_object(f.readline())
    eo  = obj._narrow(_GlobalIDL.Echo)
    
    if eo is None:
        print "Object reference is not an Echo"
        sys.exit(1)
    message = raw_input("Write message here:")
    try:
        result  = eo.echoString(message)
        print "Запрос: '%s'. Ответ: '%s'." % (message,result)
    except:
        print "Error"


def record(x):
    if (tkMessageBox.askyesno("Library", "The lib is not connected. Do you want to do it now?")):
        op = tkFileDialog.askopenfilename()
        if op[-3:]!='dll':
            print tkMessageBox.showerror('Error', "The library should have dll extension!")
            return 0

        x = open(op,'r').readlines()
        try:
            c.execute("DELETE FROM Dll WHERE MotherWell='" + x[1][:-1] +"'")
            c.execute("INSERT INTO Dll(DllName, DllPath, MotherWell) "
                          + "VALUES ('" + x[0][:-1] + "', '" + op + "', '" + x[1][:-1] + "')")
            conn.commit()
            return True
        except:
            print "Bad dll"
            return False
        return agent(x)


def agent(x):
    for row in c.execute('SELECT * FROM Dll'):
        if row[3]==x:
            if os.path.isfile(row[2]):
                return True
    return False


def nodll():
    for row in c.execute('SELECT * FROM Dll'):
        if row[2]!='None':
            return False
    return True


def get1dll():
    if nodll():
        if (tkMessageBox.askyesno("Library", "There is no connected lib. Do you want to do it now?")):
            op = tkFileDialog.askopenfilename()
            if op[-3:]!='dll':
                tkMessageBox.showerror('Error', "The library should have dll extension!")
                return False

            x = open(op,'r').readlines()
            try:
                c.execute("DELETE FROM Dll WHERE MotherWell='" + x[1][:-1] +"'")
                c.execute("INSERT INTO Dll(DllName, DllPath, MotherWell) "
                          + "VALUES ('" + x[0][:-1] + "', '" + op + "', '" + x[1][:-1] + "')")
                conn.commit()
                return True
            except:
                print "Bad dll"
                return False
    else:
        return True


def callback(event):
    if tree.selection()[0][0:2] == '_W':
        if agent(tree.selection()[0][2:]):
            Client()
        else:
            if (record(tree.selection()[0][2:])):
                Client()


def listfunction(event):
    win = Toplevel()
    # display message
    tkMessageBox.message = "This window keeps VERY SECRET INFORMATION"
    Label(win, text=tkMessageBox.message).pack()
    # quit child window and return to root window
    # the button is optional here, simply use the corner x of the child window
    Button(win, text='OK', command=win.destroy).pack()


def adddll():
    if True:
        if True:
            op = tkFileDialog.askopenfilename()
            if op[-3:]!='dll':
                print tkMessageBox.showerror('Error', "The library should have dll extension!")
                return False

            x = open(op,'r').readlines()
            print x
            try:
                c.execute("DELETE FROM Dll WHERE MotherWell='" + x[1][:-1] +"'")
                c.execute("INSERT INTO Dll(DllName, DllPath, MotherWell) "
                          + "VALUES ('" + x[0][:-1] + "', '" + op + "', '" + x[1][:-1] + "')")
                conn.commit()
                return True
            except:
                print "Bad dll"
                return False

def removedlls():
    tkMessageBox.showinfo('Ok', "Please go to console")

    raw_input("Are you ready? Press enter")
    for i in c.execute("SELECT * FROM Dll"):
        print i[1] + "\nMother bush:" + i[3]

    s = raw_input("Enter the name of dll to remove it:")
    c.execute("DELETE FROM Dll WHERE DllName ='" + s + "'")
    conn.commit()
    print "Success"
    
if __name__ == "__main__":
    #CreateTable()

    root = Tk()
    root.resizable(width=False, height=False)
    root.geometry('{}x{}'.format(400, 200))

    conn = sqlite3.connect('good.db')
    c = conn.cursor()
    
    if get1dll():
        menubar = Menu(root)
        menubar.add_command(label="Add library", command=adddll)
        menubar.add_command(label="Remove library", command=removedlls)
        menubar.add_command(label="Quit", command=root.quit)

        root.config(menu=menubar)
        tree = ttk.Treeview(root)
        tree.pack()
        for row in c.execute('SELECT * FROM Deposit'):
            tree.insert('', str(row[0]), '_D' + str(row[1]), text = str(row[1]))

        for row in c.execute('SELECT * FROM Bush'):
            tree.insert('_D' + str(row[2]), str(row[0]), '_B' + str(row[1]), text = str(row[1]))

        for row in c.execute('SELECT * FROM Well'):
            tree.insert('_B' + str(row[2]), str(row[0]), '_W' + str(row[1]), text = str(row[1]))

        tree.bind('<<TreeviewSelect>>', callback)

        lb = Listbox(root)
        lb.pack()
        
        lb.place(x=199, y=0, height=200, width=200)
        tree.place(x=0, y=0, height=200, width=200)

        lb.bind("<Double-Button-1>", listfunction)

        root.mainloop()
    conn.close()
