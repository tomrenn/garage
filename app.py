import socket, threading
from time import sleep
from flask import Flask, request, redirect
from gpiozero import OutputDevice
from gpiozero.pins.mock import MockPin
app = Flask(__name__)

ip = socket.gethostbyname(socket.gethostname())
host = socket.gethostname()
print(ip)
print(host)
is_raspberry_pi = host == 'raspberrypi'

pin = 4
if not is_raspberry_pi:
    print('USING MOCK PIN')
    pin = MockPin(pin)

relay = OutputDevice(pin)

def toggleRelay():
    relay.toggle()
    sleep(1)
    relay.toggle()

@app.route('/garage', methods=['GET', 'POST'])
def garage():
    redirect_addr = request.args.get('referer')

    if request.method == 'POST':
        print('POST')
        print(request.headers)
        t = threading.Thread(target=toggleRelay)
        t.daemon = True
        t.start()
    else:
        print('GET')


    if redirect_addr:
        return redirect(redirect_addr + "#success")
    return 'OK'

if is_raspberry_pi:
    app.run(host='0.0.0.0', threaded=True)
else:
    app.run()
