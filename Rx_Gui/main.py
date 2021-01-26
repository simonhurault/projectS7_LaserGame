from tkinter import *
from Rx_gui import *
from stm32_com import*



def create_menu_bar(window):
    menu_bar = Menu()

    menu_help = Menu(menu_bar, tearoff=0)
    menu_help.add_command(label="How to use", command=do_about)
    menu_help.add_command(label="Get good Com port", command=com_info)
    menu_bar.add_cascade(label="Help", menu=menu_help)

    window.config(menu=menu_bar)


def do_about():
    messagebox.showinfo("How to use", "1) Put the com and baud rate of the serial link.\n"
                                      "2) Please be aware that changing Com don't kill previous com.\n"
                                      "3) Enable receive info to print data\n"
                                      "4) Data should appear on scrolled text part\n")


def com_info():
    messagebox.showinfo("Where to find com port", "You can find the Stm port in the Device Manager in Port section.\n\n"
                                                "Vous pouvez trouver le port com de la Stm dans le gestionnaire de"
                                                " peripheriques dans la section Port.\n\n"
                                                  "Si vous etes au bat14 utilisez dvgmt.")


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


window = Tk()  # We create the main window
window.title("Laser game")

rx = RxWindow(window)  # The rx frame

create_menu_bar(window)


buttonDestroy = Button(window, text=" Quit ", command=quit_application, bg='Red', cursor='hand2')
buttonDestroy.grid(row=3, column=0)

window.mainloop()   # create the loop

