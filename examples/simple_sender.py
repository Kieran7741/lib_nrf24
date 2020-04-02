import RPi.GPIO as GPIO
from nrf24 import NRF24, convert_message_to_bytes
import spidev

import time

GPIO.setmode(GPIO.BCM)

# Read and Write pips
pipes = [[0xe7, 0xe7, 0xe7, 0xe7, 0xe7],
         [0xc2, 0xc2, 0xc2, 0xc2, 0xc2]]
# Initialize radio
radio = NRF24(GPIO, spidev.SpiDev())
radio.begin(0, ce_pin=17)

# Set the payload size
radio.setPayloadSize(32)

# Set communication channel. Must be the same between talking radios
radio.setChannel(0x60)
radio.setDataRate(NRF24.BR_2MBPS)
radio.setPALevel(NRF24.PA_MIN)
radio.setAutoAck(True)
radio.enableDynamicPayloads()
radio.enableAckPayload()

# Set up reading pipe as this is the receiver
radio.openWritingPipe(pipes[0])
# Print all configuration values of radio
radio.printDetails()

# Not listening because we are sending
# radio.startListening()

while True:
    message = list('From sender')
    print('Sending message to receiver')
    radio.write(message)
    print('Message sent')

    if radio.isAckPayloadAvailable():
        returned_payload = []
        radio.read(returned_payload, radio.getDynamicPayloadSize())
        print('Payload received: {}'.format(returned_payload))
    else:
        print('No payload received')
    time.sleep(1)

