import serial
from threading import Thread


class Server(Thread):
    """
    This class will create the server that will receive the frames
    To receive the message on another script create the Server by giving a function that will use the message receive
    """
    def __init__(self, change_laser_rx, com, baud_rate):  # Port = int, change_text_frame = function
        Thread.__init__(self)  # Here we create another thread for the server
        # Connect the serial port
        self.serialPort = serial.Serial(com, baud_rate, timeout=0)
        self.changeLaserRx = change_laser_rx;

    def server_thread(self):
        """
        receive the data from the serial port, put it on the console and
        send it to gui
        :return:
        """
        while True:
            if self.serialPort.isOpen():
                data = self.serialPort.read(5)  # serial read 20-bit data
                laser = data
                if laser != b"":
                    self.changeLaserRx(laser)
            else:
                print("\nSerial port is closed")

    def run(self):
        """
        This method is the one that will be launch in the server thread
        """
        receive_thread = Thread(target=self.server_thread)
        receive_thread.start()

