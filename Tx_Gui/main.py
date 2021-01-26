from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import os
import serial
import csv
import numpy as np


def create_menu_bar(window):
    menu_bar = Menu()

    menu_help = Menu(menu_bar, tearoff=0)
    menu_help.add_command(label="How to use", command=do_about)
    menu_help.add_command(label="Get good Com port", command=com_info)
    menu_bar.add_cascade(label="Help", menu=menu_help)

    menu_file = Menu(menu_bar, tearoff=1)
    menu_file.add_command(label="Edit laser file", command=open_file)
    menu_file.add_command(label="Refresh file", command=refresh)
    menu_bar.add_cascade(label="File", menu=menu_file)

    window.config(menu=menu_bar)


def do_about():
    messagebox.showinfo("How to use", "1) Put the com and baud rate of the serial link.\n"
                                      "2) If you use our stm32 code baud rate should be 115200\n"
                                      "3) Pick a laser number. The numbers and associated PWM values are on "
                                      "laser_init.txt\n"
                                      "4) Use send button to set the laser number\n")


def com_info():
    messagebox.showinfo("Where to find com port", "You can find the Stm port in the Device Manager in Port section.\n\n"
                        "Vous pouvez trouver le port com de la Stm dans le gestionnaire de"
                        " peripheriques dans la section Port.\n\nSi vous etes au bat14 utilisez dvgmt.")


def open_file():
    os_command_string = "notepad.exe ../laser_init.txt"
    os.system(os_command_string)


def refresh():
    refresh_file()
    refresh_combobox()


def refresh_file():
    global lasers_PWM_values
    global lasers_number
    lasers_number = []
    lasers_PWM_values = []
    with open('../laser_init.txt') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                print(f'Laser\t{row[0]} has {row[1]} value')
                lasers_number.append(row[0])
                lasers_PWM_values.append(row[1])
                line_count += 1
        print(f'There is {line_count - 1} lasers.')


def refresh_combobox():
    global comboLaser
    comboLaser.destroy()
    comboLaser = ttk.Combobox(window, values=lasers_number, width=8)
    comboLaser.grid(column=1, row=5)


def quit_application():
    """
    destroy the current window
    """
    result = messagebox.askquestion("Quit", "Are you sure you want to quit?", icon='warning', type='yesnocancel')
    if result == 'yes':
        window.destroy()
    elif result == 'no':
        return
    elif result == 'cancel':
        return


def send_data():
    global entree_com
    global entree_baud
    global comboLaser
    global window
    try:
        serial_port = serial.Serial("Com" + entree_com.get(), entree_baud.get(), timeout=2)
    except serial.serialutil.SerialException or ValueError:
        print("impossible to open Com port")
        com_ok_txt = Label(window, text="Failure", bg="Red", width=10)
        com_ok_txt.grid(row=5, column=0, columnspan=1, sticky=W)
        messagebox.showerror(title='Error', message='Impossible to open com port')
        return
    com_ok_txt = Label(window, text="Done", bg="Green", width=10)
    com_ok_txt.grid(row=5, column=0, columnspan=1, sticky=W)
    data = 0x00000000
    if serial_port.isOpen():
        print("Serial port is open")
        data = lasers_PWM_values[int(comboLaser.get()) - 1]  # data sent
        print("Data : ", data)
        serial_port.write(data.encode())  # Serial port write data
        print("\nyou send data:", data)


    # Close the serial port
    serial_port.close()
    if serial_port.isOpen():
        print("Serial port is not closed")
    else:
        print("Serial port is closed")


# Reading of csv file
lasers_number = []
lasers_PWM_values = []
refresh_file()


window = Tk()  # We create the main window
window.title("Laser game setup")


create_menu_bar(window)

# Communication widgets
setTxt = Label(window, text="Communication set : ")
setTxt.grid(row=1, column=0)

comTxt = Label(window, text="Com : ")
comTxt.grid(row=3, column=0, columnspan=1, sticky=W)

entree_com = Entry(window, width=8)
entree_com.grid(row=3, column=1, columnspan=4)

baudRateTxt = Label(window, text="Baud rate : ")
baudRateTxt.grid(row=4, column=0, columnspan=1, sticky=W)

entree_baud = Entry(window, width=8)
entree_baud.grid(row=4, column=1, columnspan=4)

laserTxt = Label(window, text="Laser value : ")
laserTxt.grid(row=5, column=0, columnspan=1, sticky=W)

comboLaser = ttk.Combobox(window, values=lasers_number, width=8)
comboLaser.grid(column=1, row=5)

buttonSend = Button(window, text=" Send ", command=send_data,
                         bg='Green2', cursor='hand2')
buttonSend.grid(row=6, column=1, sticky=W)

buttonDestroy = Button(window, text=" Quit ", command=quit_application, bg='Red', cursor='hand2')
buttonDestroy.grid(row=7, column=1, sticky=W)

window.mainloop()   # create the loop

