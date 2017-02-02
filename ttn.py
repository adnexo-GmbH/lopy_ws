from network import LoRa
import socket
import binascii
import struct


# Update these values according to your ABP registration
DEV_ADDR = 'XXXXXXXX'
NWK_SWKEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
APP_SWKEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

# Initialize LoRa in LORAWAN mode.
lora = LoRa(mode=LoRa.LORAWAN)


# create an ABP authentication params
dev_addr = struct.unpack(">l", binascii.unhexlify(DEV_ADDR))[0]
nwk_swkey = binascii.unhexlify(NWK_SWKEY)
app_swkey = binascii.unhexlify(APP_SWKEY)

# join a network using ABP (Activation By Personalization)
lora.join(activation=LoRa.ABP, auth=(dev_addr, nwk_swkey, app_swkey))

# create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

# make the socket blocking
# (waits for the data to be sent and for the 2 receive windows to expire)
s.setblocking(True)

# send some data
s.send(bytes([0x01, 0x02, 0x03]))

# make the socket non-blocking
# (because if there's no data received it will block forever...)
s.setblocking(False)

# get any data received (if any...)
data = s.recv(64)
print(data)
