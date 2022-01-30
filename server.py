import os
import serial.tools.list_ports
import threading
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler


def httpServerFunction(httpd):
    print("HTTP server: http://localhost:8000/")
    httpd.serve_forever()


def connectToArduino():
    ports = serial.tools.list_ports.comports()
    portsList = []
    num = 1

    for port, desc, hwid in sorted(ports):
        print("[{}] {}: {}".format(num, port, desc))
        portsList.append(port)
        num += 1

    n = int(input('Select port: '))

    if n > len(portsList):
        print("Invalid number!")
        exit()

    print("Opening Arduino connection...")
    return serial.Serial(portsList[n - 1], 9600)


def handleArduinoConnection(arduinoSerial):
    if os.path.exists("data.txt"):
        os.remove("data.txt")

    while True:
        data = arduinoSerial.readline()
        text = data.decode('Ascii').strip()

        if len(text) > 0:
            currentTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            with open('data.txt', 'a+') as file:
                file.write(currentTime + ";" + text + '\n')

            print(text)


def main():
    arduinoSerial = connectToArduino()

    httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
    httpServerThread = threading.Thread(target=httpServerFunction, args=(httpd,))
    httpServerThread.start()

    try:
        handleArduinoConnection(arduinoSerial)
    except KeyboardInterrupt:
        print("Closing Arduino connection...")
        arduinoSerial.close()

        print("HTTP server shutdown...")
        httpd.shutdown()
        httpServerThread.join()


if __name__ == '__main__':
    main()
