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
radio.openReadingPipe(1, pipes[1])
# Print all configuration values of radio
radio.printDetails()

radio.startListening()

while True:
    ack_payload = [1]

    # Wait for incoming data
    while not radio.available(0):
        time.sleep(.01)

    # Note: All data transfer is in bytes
    recieved_message = []
    radio.read(recieved_message, radio.getDynamicPayloadSize())
    print('Message as bytes: {0}'.format(recieved_message))
    converted_message = convert_message_to_bytes(recieved_message)
    print('Message as string: {}'.format(converted_message))

    # Send ack payload back to sender
    radio.writeAckPayload(1, ack_payload, len(ack_payload))
    print('Ack Payload sent back to sender')
