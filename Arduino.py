from multiprocessing import Process
import serial
import serial.tools.list_ports
import time

# Ce fichier sera celui qui detectera l'arduino et ses touches
ports = list(serial.tools.list_ports.comports())
puerto = ""
for p in ports:
    if "Arduino" in p[1]:
        puerto = p[0]
        break

def escuchar():
    ser = serial.Serial(puerto, 9600)
    while True:
        x = chr(ser.readline()[0])
        print(x)


def run():
    print("Init")

    prc = Process(target=escuchar())
    prc.start()


if __name__ == '__main__':
    run()
