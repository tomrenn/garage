import socket, threading
from time import sleep
from flask import Flask, request
from gpiozero import OutputDevice
from gpiozero.pins.mock import MockPin
app = Flask(__name__)

ip = socket.gethostbyname(socket.gethostname())

pin = 4
if (ip != '192.168.29.29'):
    pin = MockPin(pin)

relay = OutputDevice(pin)

def toggleRelay():
    relay.toggle()
    sleep(1)
    relay.toggle()

@app.route('/garage', methods=['GET', 'POST'])
def garage():
    if request.method == 'POST':
        print('POST')
        t = threading.Thread(target=toggleRelay)
        t.daemon = True
        t.start()
    else:
        print('GET')

    return 'OK'

app.run()
