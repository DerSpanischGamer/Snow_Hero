import serial
import time

# Ce fichier sera celui qui detectera l'arduino et ses touches

ser = serial.Serial('COM4', 9600)
while True:
    time.sleep(0.001)
    print(t)
