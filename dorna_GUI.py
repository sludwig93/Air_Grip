from dorna_functions import *

from tkinter import *

import time

joints = ['j0','j1','j2','j3','j4']
joint_vals = dorna_position()



def j0_position():
    global locateFlag, j0_current
    loc = dorna_locate()
    j0_current = loc[0]
    return j0_current


def close_window():
    window.destroy()

def halt():
    robot.move({'path':'joint','movement':0},append = False, fulfill = True)

def move_0():
    deg = limit180(float(txt_0.get()))
    robot.move({'path':'joint','movement':0,'j0':deg})
    joint_vals[0] = deg

def clicked_0():
    try:
        joint_vals[0] = limit180(float(txt_0.get()))
        update = joints[0] + ' currently at ' + str(joint_vals[0])
        lbl_0.configure(text=update)

    except ValueError:
        print('You must enter a number.')

def clicked_1():
    try:
        if float(txt_1.get()) > -360 and float(txt_1.get()) <= 360: 
            joint_vals[1] = float(txt_1.get())
            update = joints[1] + ' currently at ' + str(joint_vals[1])
            lbl_1.configure(text=update)
        else:
            print('Value must be between -360 and 360.')
    except ValueError:
        print('You must enter a number.')

def clicked_2():
    try:
        if float(txt_2.get()) > -360 and float(txt_2.get()) <= 360: 
            joint_vals[2] = float(txt_2.get())
            update = joints[2] + ' currently at ' + str(joint_vals[2])
            lbl_2.configure(text=update)
        else:
            print('Value must be between -360 and 360.')
    except ValueError:
        print('You must enter a number.')

def clicked_3():
    try:
        if float(txt_3.get()) > -360 and float(txt_3.get()) <= 360: 
            joint_vals[3] = float(txt_3.get())
            update = joints[3] + ' currently at ' + str(joint_vals[3])
            lbl_3.configure(text=update)
        else:
            print('Value must be between -360 and 360.')
    except ValueError:
        print('You must enter a number.')

def clicked_4():
    try:
        if float(txt_4.get()) > -360 and float(txt_4.get()) <= 360: 
            joint_vals[4] = float(txt_4.get())
            update = joints[4] + ' currently at ' + str(joint_vals[4])
            lbl_4.configure(text=update)
        else:
            print('Value must be between -360 and 360.')
    except ValueError:
        print('You must enter a number.')



window = Tk()

window.title('Dorna User Interface')
window.geometry('500x300')

con = Button(window, text = 'Connect Robot', font=('Times New Roman', 20), command=dorna_connect)
con.grid(column=0,row=0)

home = Button(window, text = 'Home Robot', font=('Times New Roman', 20), command=dorna_startup)
home.grid(column=1,row=0)

halt_button = Button(window, text = 'STOP', font=('Times New Roman', 20), fg = 'red', bg = 'black', command=robot.halt)
halt_button.grid(column=2,row=0)

reset = Button(window, text = 'Reset Position', font=('Times New Roman', 20), command=dorna_reset)
reset.grid(column=0,row=6)

disconnect = Button(window, text = 'Disconnect', font=('Times New Roman', 20), \
                    command= combine_funcs(dorna_disconnect,close_window))
disconnect.grid(column=1,row=6)

lbl_0 = Label(window, text = 'j0 currently at ' + str(joint_vals[0]), font=('Times New Roman', 16))
lbl_0.grid(column=0,row=1)
txt_0 = Entry(window, width=10)
txt_0.grid(column=1,row=1)
btn_0 = Button(window, text = 'Update value', font=('times new roman',12), command= combine_funcs(move_0, clicked_0))
btn_0.grid(column=2,row=1)

lbl_1 = Label(window, text = 'j1 currently at ' + str(joint_vals[1]), font=('Times New Roman', 16))
lbl_1.grid(column=0,row=2)
txt_1 = Entry(window, width=10)
txt_1.grid(column=1,row=2)
btn_1 = Button(window, text = 'Update value', font=('times new roman',12), command=clicked_1)
btn_1.grid(column=2,row=2)

lbl_2 = Label(window, text = 'j2 currently at ' + str(joint_vals[2]), font=('Times New Roman', 16))
lbl_2.grid(column=0,row=3)
txt_2 = Entry(window, width=10)
txt_2.grid(column=1,row=3)
btn_2 = Button(window, text = 'Update value', font=('times new roman',12), command=clicked_2)
btn_2.grid(column=2,row=3)

lbl_3 = Label(window, text = 'j3 currently at ' + str(joint_vals[3]), font=('Times New Roman', 16))
lbl_3.grid(column=0,row=4)
txt_3 = Entry(window, width=10)
txt_3.grid(column=1,row=4)
btn_3 = Button(window, text = 'Update value', font=('times new roman',12), command=clicked_3)
btn_3.grid(column=2,row=4)

lbl_4 = Label(window, text = 'j4 currently at ' + str(joint_vals[4]), font=('Times New Roman', 16))
lbl_4.grid(column=0,row=5)
txt_4 = Entry(window, width=10)
txt_4.grid(column=1,row=5)
btn_4 = Button(window, text = 'Update value', font=('times new roman',12), command=clicked_4)
btn_4.grid(column=2,row=5)

window.mainloop()

