from machine import UART
import utime as time

import adafruit_gps

# Create a GPS module instance.
#uart = UART(1, baudrate=9600, timeout_chars=3000, pins=('P8','P2'))
#uart = UART(1, baudrate=9600)
# Create a GPS module instance.
uart = UART(1,9600, pins = ('P22','P21'))
uart.init(baudrate=9600, bits=8, parity=None, stop=1, pins=('P22', 'P21'))
print('UART')
print(uart)

gps = adafruit_gps.GPS(uart)
gps.send_command('PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
gps.send_command('PMTK220,1000')
last_print = time.ticks_ms()

while True:
    gps.update()
    current = time.ticks_ms()
    if current - last_print >= 1.0:
        last_print = current
        if not gps.has_fix:
            print('Waiting for fix...')
            continue
        print('=' * 40) # Print a separator line.
        print('Latitude: {0:.6f} degrees'.format(gps.latitude))
        print('Longitude: {0:.6f} degrees'.format(gps.longitude))