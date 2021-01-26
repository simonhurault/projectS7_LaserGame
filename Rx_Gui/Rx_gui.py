from tkinter import *
from tkinter.scrolledtext import ScrolledText
from stm32_com import*
from tkinter import messagebox
import csv


class RxWindow:
    """
    This class create an object that will manage the graphical interface of the Rx.py script
    """

    def __init__(self, window):  # mainWindow= Tk()
        self._create_rx_frame(window)
        self._create_com_frame(window)
        self.number_laser = 0
        self.number_valid_laser = 0
        self.number_invalid_laser = 0

    def _create_rx_frame(self, rx_window):
        """
        create rx part of gui
        :param rx_window:
        :return: void
        """
        self.window = Frame(rx_window)  # we create a special Frame on the main window for the rx frames
        self.window.grid(row=0, column=0)

        self.printRec = False

        self.logText = ScrolledText(self.window, width=70)  # log text
        self.logText.grid(row=1, column=1)

        self.buttonStart = Checkbutton(self.window, text=" Receive info ", command=self.change_receive, bg='bisque',
                                       cursor='hand2')
        self.buttonStart.grid(row=3, column=1)

        self.buttonClear = Button(self.window, text=" Clear ", command=self.clear, cursor='hand2')
        self.buttonClear.grid(row=4, column=1)

        self.buttonConnect = Button(self.window, text=" Set Com ", command=self.clear, cursor='hand2')
        self.buttonClear.grid(row=4, column=1)

        self.logText.insert(END, "Detected lasers :" + '\n')

    def _create_com_frame(self, right_frame):
        """
        create com part of gui
        :param right_frame:
        :return: void
        """
        self.window = Frame(right_frame)  # we create a special Frame on the main window for the tx frames
        self.window.grid(row=0, column=1)

        self.setTxt = Label(self.window, text="Communication set : ")
        self.setTxt.grid(row=1, column=0)

        self.comTxt = Label(self.window, text="Com : ")
        self.comTxt.grid(row=3, column=0, columnspan=1, sticky=W)

        self.entree_com = Entry(self.window, width=8)
        self.entree_com.grid(row=3, column=1, columnspan=4)

        self.baudRateTxt = Label(self.window, text="Baud rate : ")
        self.baudRateTxt.grid(row=4, column=0, columnspan=1, sticky=W)

        self.entree_baud = Entry(self.window, width=8)
        self.entree_baud.grid(row=4, column=1, columnspan=4)

        self.buttonSet = Button(self.window, text=" Set parameters ", command=self.set_communication,
                                 bg='Green2', cursor='hand2')
        self.buttonSet.grid(row=5, column=1, sticky=W)

    def change_laser_rx(self, laser_received):
        """
        This method is called by the server to print the incomming laser
        :param message_received: bytes, the message that the server received
        """
        self.print_laser(laser_received)

    def change_receive(self):
        """
        Change the value of the wantReceive attribut and the button to start/stop the receiving of the frames
        """
        self.printRec = not self.printRec

    def print_laser(self, laser):
        """
        Print the laser id on the scrolled text
        :param frame: FrameRx object
        """
        if self.printRec:
            self.logText.insert(2.0, "\n" "\n")
            print("laser value : ", laser)
            num_laser = self.get_laser_number(int(laser))
            self.number_laser += 1
            if num_laser == -1:
                self.logText.insert(2.0, "Laser unknown")
                self.number_invalid_laser += 1
            else:
                self.logText.insert(2.0, num_laser)
                self.logText.insert(2.0, "Laser ")
                self.number_valid_laser += 1
            self.logText.insert(3.0, "\nAt the moments results are : " + str(self.number_laser) + " laser(s)\n" + str(self.number_valid_laser)
                            + " were valid and " + str(self.number_invalid_laser) + " were invalid\n")
            self.logText.insert(2.0, "\n --------------------------------------------------------------------\n\n")


    @staticmethod
    def get_laser_number(laser):
        """
        get the laser number looking to data get in laser_init.txt
        :param laser:
        :return: laser number
        """
        global lasers_PWM_values
        global lasers_number
        index = 0
        for laser_value in lasers_PWM_values:
            print("compared laser : ", int(laser_value))
            if laser * 1.05 >= int(laser_value) >= laser * 0.95:  # Tolerance of 5%
                return lasers_number[index]
            index += 1
        return -1

    def clear(self):
        """
        Clear the text area
        """
        self.logText.delete(2.0, END)

    def set_communication(self):
        com_done = True
        try:
            server = Server(self.change_laser_rx, "Com" + self.entree_com.get(), int(self.entree_baud.get()))
        except serial.serialutil.SerialException or ValueError:
            com_done = False
        if com_done:
            server.start()
            com_ok_txt = Label(self.window, text="Done", bg="Green", width=10)
            com_ok_txt.grid(row=5, column=0, columnspan=1, sticky=W)
        else:
            com_ok_txt = Label(self.window, text="Failure", bg="Red", width=10)
            com_ok_txt.grid(row=5, column=0, columnspan=1, sticky=W)
            messagebox.showerror(title='Error', message='Impossible to open com port')

# Reading of csv file
lasers_number = []
lasers_PWM_values = []
with open('../laser_init.txt') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            print(f'Laser\t{row[0]} as {row[1]} value')
            lasers_number.append(row[0])
            lasers_PWM_values.append(row[1])
            line_count += 1
    print(f'There is {line_count} lasers.')