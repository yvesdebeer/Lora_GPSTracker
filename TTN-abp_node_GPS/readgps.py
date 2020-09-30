from machine import UART, Pin
#from micropyGPS import MicropyGPS
import time

# This function have again internaly default value for RX/TX pin according to pycom documentation -> 
# uart.init(baudrate=9600, bits=8, parity=None, stop=1, * , timeout_chars=2, pins=(TXD, RXD, RTS, CTS))
uart = UART(1,9600, pins = ('P22','P21'))
uart.init(baudrate=9600, bits=8, parity=None, stop=1, pins=('P22', 'P21'))

while(True):
    if(uart.any()):
        a = uart.read(100)
        print(a)
#    else:
#        print("No data")