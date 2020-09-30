import binascii
import pycom
import socket
import time
from network import LoRa

# Colors
off = 0x000000
red = 0x7f0000
green = 0x007f00
blue = 0x00007f

# Turn off hearbeat LED
pycom.heartbeat(False)

# Initialize LoRaWAN radio
lora = LoRa(mode=LoRa.LORAWAN)

# Set network keys
app_eui = binascii.unhexlify('70B3D57EF00046BB')
app_key = binascii.unhexlify('4A0B7E09CA5438152D054DB89513736D')

# Join the network
lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0, dr=0)
pycom.rgbled(0x1f0000)

# Loop until joined
while not lora.has_joined():
    print('Not OTAA joined yet...')
    pycom.rgbled(0x1f0000)
    time.sleep(0.1)
    pycom.rgbled(off)
    time.sleep(2.4)

print('OTAA Joined')
pycom.rgbled(0x00001f)

s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)
s.setblocking(True)

i = 0
while True:
    pycom.rgbled(0x00003f)
    count = s.send(bytes([i % 256]))
    print('Sent %s bytes' % count)
    time.sleep(0.1)
    pycom.rgbled(0x001f00)
    time.sleep(59.9)
    i += 1