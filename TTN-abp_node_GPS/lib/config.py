""" LoPy LoRaWAN Nodeconfiguration options """
from array import array

DEBUG = 1

WIFI_SSID = 'wifi9'
WIFI_PASS = '42805WPA2'
WIFI_IP = '<replace with your values>' # fixed IP
WIFI_SUBNET = '<replace with your values>'
WIFI_GATEWAY = '<replace with your values>'
WIFI_DNS1 = '<replace with your values>'

# TTN
# These you need to replace!
DEV_ADDR = '<replace with your values>'
NWK_SWKEY = '<replace with your values>'
APP_SWKEY = '<replace with your values>'

# set the port, one is used during debugging
# you can filter that port out in the TTN mapper integration
TTN_FPort_debug = 1
TTN_FPort = 2

# CREATE LOG?
LOG = 1
FILENAME = 'log.txt'

# GPS UART connection
TX = "P11"
RX = "P12"

# TIMEZONE / DAYLIGHT SAVING
TIMEZONE = 1
DAYLIGHT = 1

# GPS SPEED variables
AUTO = 0
STAT = 1
WALK = 2
CYCLE = 3
CAR = 4

# update speed in seconds
UPDATE = array('H', [30,30,20,10,10])
MAXSPEED = array('H', [0,1,6,30,150])

""" LoPy LoRaWAN Nano Gateway configuration options """

import machine
import ubinascii

WIFI_MAC = ubinascii.hexlify(machine.unique_id()).upper()
# Set  the Gateway ID to be the first 3 bytes of MAC address + 'FFFE' + last 3 bytes of MAC address
GATEWAY_ID = WIFI_MAC[:6] + "FFFE" + WIFI_MAC[6:12]

SERVER = 'router.eu.thethings.network'
PORT = 1700

NTP = "pool.ntp.org"
NTP_PERIOD_S = 3600

# for EU868
LORA_FREQUENCY = 868100000
LORA_GW_DR = "SF7BW125" # DR_5
LORA_NODE_DR = 5

# for US915
# LORA_FREQUENCY = 903900000
# LORA_GW_DR = "SF10BW125" # DR_0
# LORA_NODE_DR = 0
