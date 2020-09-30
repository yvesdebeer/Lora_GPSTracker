from network import LoRa
import socket
import binascii
import struct
import time
import config

from machine import UART
import utime as time
import adafruit_gps

# initialize LoRa in LORAWAN mode.
# Please pick the region that matches where you are using the device:
# Asia = LoRa.AS923
# Australia = LoRa.AU915
# Europe = LoRa.EU868
# United States = LoRa.US915
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868, tx_power=20, tx_retries=3)
# create an ABP authentication params
dev_addr = struct.unpack(">l", binascii.unhexlify('26011F35'))[0]
nwk_swkey = binascii.unhexlify('2D758A1E13810A307A088F9F558A0D2D')
app_swkey = binascii.unhexlify('509594BFC29B1EE2A8165C6ACAE06855')
# remove all the non-default channels
for i in range(3, 16):
    lora.remove_channel(i)
# set the 3 default channels to the same frequency
lora.add_channel(0, frequency=config.LORA_FREQUENCY, dr_min=0, dr_max=5)
lora.add_channel(1, frequency=config.LORA_FREQUENCY, dr_min=0, dr_max=5)
lora.add_channel(2, frequency=config.LORA_FREQUENCY, dr_min=0, dr_max=5)
# join a network using ABP (Activation By Personalization)
lora.join(activation=LoRa.ABP, auth=(dev_addr, nwk_swkey, app_swkey))
# create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
# set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, config.LORA_NODE_DR)
# make the socket non-blocking
s.setblocking(False)


# Create a GPS module instance.
#uart = UART(1, baudrate=9600, timeout_chars=3000, pins=('P8','P2'))
#uart = UART(1, baudrate=9600)
uart = UART(1,9600, pins = ('P22','P21'))
uart.init(baudrate=9600, bits=8, parity=None, stop=1, pins=('P22', 'P21'))
# Create a GPS module instance.
gps = adafruit_gps.GPS(uart)
print(gps)
# Turn on the basic GGA and RMC info (what you typically want)
gps.send_command('PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
# Set update rate to once a second (1hz) which is what you typically want.
gps.send_command('PMTK220,1000')

last_print = time.ticks_ms()

while True:
    # Make sure to call gps.update() every loop iteration and at least twice
    # as fast as data comes from the GPS unit (usually every second).
    # This returns a bool that's true if it parsed new data (you can ignore it
    # though if you don't care and instead look at the has_fix property).
    gps.update()
    # Every second print out current location details if there's a fix.
    current = time.ticks_ms()
    if current - last_print >= 1.0:
        last_print = current

        if not gps.has_fix:
            # Try again if we don't have a fix yet.
            print('Waiting for fix...')
            continue
        # We have a fix! (gps.has_fix is true)
        # Print out details about the fix like location, date, etc.
        print('=' * 40)  # Print a separator line.
        print('Fix timestamp: {}/{}/{} {:02}:{:02}:{:02}'.format(
            gps.timestamp_utc[1],   # Grab parts of the time from the
            gps.timestamp_utc[2],  # struct_time object that holds
            gps.timestamp_utc[0],  # the fix time.  Note you might
            gps.timestamp_utc[3],  # not get all data like year, day,
            gps.timestamp_utc[4],   # month!
            gps.timestamp_utc[5]))
        print('Latitude: {} degrees'.format(gps.latitude))
        print(gps.latitude)
        print('Longitude: {} degrees'.format(gps.longitude))
        print('Fix quality: {}'.format(gps.fix_quality))
        # Some attributes beyond latitude, longitude and timestamp are optional
        # and might not be present.  Check if they're None before trying to use!
        if gps.satellites is not None:
            print('# satellites: {}'.format(gps.satellites))
        if gps.altitude_m is not None:
            print('Altitude: {} meters'.format(gps.altitude_m))
        if gps.track_angle_deg is not None:
            print('Speed: {} knots'.format(gps.speed_knots))
        if gps.track_angle_deg is not None:
            print('Track angle: {} degrees'.format(gps.track_angle_deg))
        if gps.horizontal_dilution is not None:
            print('Horizontal dilution: {}'.format(gps.horizontal_dilution))
        if gps.height_geoid is not None:
            print('Height geo ID: {} meters'.format(gps.height_geoid))

        pkt = '{},{}'.format(gps.latitude,gps.longitude)
        print('Sending:', pkt)
        s.send(pkt)
        rx, port = s.recvfrom(256)
        if rx:
            print('Received: {}, on port: {}'.format(rx, port))
        #put GPS in Standby mode
        gps.send_command('PMTK161,0')
        #time.sleep(4)
        machine.deepsleep(300000)
