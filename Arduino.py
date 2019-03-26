import serial
import time
import Main

# Ce fichier sera celui qui detectera l'arduino et ses touches

ser = serial.Serial('/dev/tty.usbserial', 9600)
while True:
    time.sleep(0.001)
    print ser.readline()
